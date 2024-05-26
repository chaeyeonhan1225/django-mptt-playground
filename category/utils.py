from django.db.models import QuerySet, F, Max
from django.db import connection

from category.models import Category, CategoryMPTT


# def get_category_path(category: Category) -> list[str]:
#     if category.parent is not None:
#         paths = get_category_path(category.parent)
#         paths.append(category.name)
#         return paths
#     return [category.name]


def get_children(category: Category) -> QuerySet[Category]:
    return Category.objects.filter(parent=category)


def save_category(name: str, parent: CategoryMPTT = None):
    if parent is None:  # 루트 노드 추가
        tree = CategoryMPTT.objects.aggregate(tree_size=Max('rgt'))
        tree_size = tree['tree_size'] or 0

        category = CategoryMPTT(name=name, lft=tree_size + 1, rgt=tree_size + 2)
        category.save()
        return category
    elif parent.is_leaf:  # parent에 신규 node를 추가하는 것이라면
        new_lft = parent.lft + 1
        new_rgt = parent.lft + 2
        CategoryMPTT.objects.filter(lft__gt=parent.rgt).update(lft=F('lft') + 2)
        CategoryMPTT.objects.filter(rgt__gt=parent.lft).update(rgt=F('rgt') + 2)

        category = CategoryMPTT(name=name, lft=new_lft, rgt=new_rgt)
        category.save()
        return category
    else:   # parent 의 children 마지막에 node 추가
        last_children = CategoryMPTT.objects.filter(lft__gt=parent.lft, rgt__lt=parent.rgt).order_by('lft').last()
        CategoryMPTT.objects.filter(lft__gt=last_children.rgt).update(lft=F('lft') + 2)
        CategoryMPTT.objects.filter(rgt__gt=last_children.rgt).update(rgt=F('rgt') + 2)

        category = CategoryMPTT(name=name, lft=last_children.rgt + 1, rgt=last_children.rgt + 2)
        category.save()
        return category


def print_tree():
    cursor = connection.cursor()
    tree_print_query = """
        SELECT CONCAT(REPEAT('  ', (COUNT(parent.name) - 1)::int), node.name) AS name, node.lft, node.rgt
        FROM categorymptt AS node,
                categorymptt AS parent
        WHERE node.lft BETWEEN parent.lft AND parent.rgt
        GROUP BY node.name, node.lft, node.rgt  ORDER BY node.lft;
        """

    cursor.execute(tree_print_query)
    rows = cursor.fetchall()

    for row in rows:
        print(f'{row[0]}{row[1], row[2]}')





