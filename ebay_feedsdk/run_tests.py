import pytest

# don't use `pytest.main()` anymore! we're getting problems here due to product_test db entity.
# please use `pytest.main(['-x', 'exporter/tests/' , 'common/tests/'])` instead!
# pytest.main(['-x', 'exporter/tests/'])
pytest.main(['-x', 'tests'])
