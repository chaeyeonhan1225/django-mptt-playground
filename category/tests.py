from django.test import TestCase

from django.db.models import Max

from category.models import CategoryMPTT
from category.utils import save_category, print_tree

# Create your tests here.
class CategoryMPTTTests(TestCase):
    def setUp(cls):
        CategoryMPTT.objects.create(name='옷', lft=1, rgt=16)
        CategoryMPTT.objects.create(name='상의', lft=2, rgt=7)
        CategoryMPTT.objects.create(name='니트', lft=3, rgt=4)
        CategoryMPTT.objects.create(name='셔츠', lft=5, rgt=6)
        CategoryMPTT.objects.create(name='하의', lft=8, rgt=13)
        CategoryMPTT.objects.create(name='바지', lft=9, rgt=10)
        CategoryMPTT.objects.create(name='치마', lft=11, rgt=12)
        CategoryMPTT.objects.create(name='원피스', lft=14, rgt=15)

    def test_테스트_데이터_확인(self):
        tree = CategoryMPTT.objects.aggregate(tree_size=Max('rgt'))
        self.assertEqual(tree['tree_size'], 16)

    def test_새로운_루트_노드_추가(self):
        category = save_category(name='테스트')

        tree = CategoryMPTT.objects.aggregate(tree_size=Max('rgt'))
        self.assertEqual(tree['tree_size'], 18)
        self.assertEqual(category.name, '테스트')
        self.assertEqual(category.lft, 17)
        self.assertEqual(category.rgt, 18)
        print_tree()

    def test_새로운_자식_노드_추가(self):
        parent = CategoryMPTT.objects.filter(name='원피스').first()
        category = save_category(name='테스트', parent=parent)

        tree = CategoryMPTT.objects.aggregate(tree_size=Max('rgt'))
        print_tree()
        self.assertEqual(tree['tree_size'], 18)
        parent.refresh_from_db()
        print(f'parent = {(parent.lft, parent.rgt)}')
        self.assertEqual(category.name, '테스트')
        self.assertEqual(category.lft, parent.lft+1)
        self.assertEqual(category.rgt, parent.rgt-1)

    def test_자식_노드_추가(self):
        parent = CategoryMPTT.objects.filter(name='상의').first()
        category = save_category(name='테스트', parent=parent)

        tree = CategoryMPTT.objects.aggregate(tree_size=Max('rgt'))
        print_tree()
        parent.refresh_from_db()
        print(f'parent = {(parent.lft, parent.rgt)}')
        self.assertEqual(category.name, '테스트')
        self.assertEqual(category.lft, parent.rgt-2)
        self.assertEqual(category.rgt, parent.rgt-1)

        category2 = save_category(name='테스트2', parent=parent)

        tree = CategoryMPTT.objects.aggregate(tree_size=Max('rgt'))
        print_tree()
        self.assertEqual(tree['tree_size'], 20)
        parent.refresh_from_db()
        print(f'parent = {(parent.lft, parent.rgt)}')

        parent = CategoryMPTT.objects.filter(name='원피스').first()
        category3 = save_category(name='테스트3', parent=parent)

        tree = CategoryMPTT.objects.aggregate(tree_size=Max('rgt'))
        print_tree()
        parent.refresh_from_db()
        print(f'parent = {(parent.lft, parent.rgt)}')

        category4 = save_category(name='테스트4', parent=parent)

        tree = CategoryMPTT.objects.aggregate(tree_size=Max('rgt'))
        print_tree()
        parent.refresh_from_db()
        print(f'parent = {(parent.lft, parent.rgt)}')

    def test_자식_노드_추가(self):
        parent = CategoryMPTT.objects.filter(name='셔츠').first()
        category = save_category(name='스트라이프 셔츠', parent=parent)

        tree = CategoryMPTT.objects.aggregate(tree_size=Max('rgt'))
        print_tree()
        parent.refresh_from_db()
        print(f'parent = {(parent.lft, parent.rgt)}')
        self.assertEqual(category.name, '스트라이프 셔츠')
        self.assertEqual(category.lft, parent.lft+1)
        self.assertEqual(category.rgt, parent.rgt-1)

        parent = CategoryMPTT.objects.filter(name='하의').first()
        category = save_category(name='반바지', parent=parent)

        tree = CategoryMPTT.objects.aggregate(tree_size=Max('rgt'))
        print_tree()
        parent.refresh_from_db()
        print(f'parent = {(parent.lft, parent.rgt)}')












