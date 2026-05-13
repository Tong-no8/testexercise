import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


# ========== 夹具 ==========
@pytest.fixture
def driver():
    """启动浏览器，先登录，测试结束后关闭"""
    print("\n[前置] 启动浏览器并登录...")
    service = Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=service)
    browser.implicitly_wait(5)
    browser.maximize_window()

    # 先登录，后续用例直接操作已登录的页面
    browser.get("https://www.saucedemo.com")
    browser.find_element(By.ID, "user-name").send_keys("standard_user")
    browser.find_element(By.ID, "password").send_keys("secret_sauce")
    browser.find_element(By.ID, "login-button").click()
    print("已登录，进入商品列表页")

    yield browser

    print("\n[后置] 关闭浏览器...")
    browser.quit()


# ========== 测试类 ==========
class TestSwagLabsCart:
    """Swag Labs 购物车与结账流程测试"""

    def test_add_item_to_cart(self, driver):
        """添加商品到购物车"""
        wait = WebDriverWait(driver, 10)

        # 记录商品名
        product_name = driver.find_element(By.CSS_SELECTOR, ".inventory_item_name").text

        # 点 Add to cart
        add_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".inventory_item:first-child .btn_inventory"))
        )
        add_btn.click()

        # 验证按钮文字变成 Remove
        btn_text = driver.find_element(By.CSS_SELECTOR, ".inventory_item:first-child .btn_inventory").text
        assert btn_text == "Remove"
        print(f"✅ 已添加商品: {product_name}，按钮变为Remove")

        # 验证购物车图标显示数量 1
        cart_badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
        assert cart_badge.text == "1"
        print("✅ 购物车数量: 1")


    def test_complete_purchase_flow(self, driver):
        """E2E：添加商品 → 购物车验证 → 结账 → 完成订单"""
        wait = WebDriverWait(driver, 10)

        # ----- 1. 添加商品 -----
        product_name = driver.find_element(By.CSS_SELECTOR, ".inventory_item_name").text
        driver.find_element(By.CSS_SELECTOR, ".inventory_item:first-child .btn_inventory").click()
        print(f"1. 已添加商品: {product_name}")

        # ----- 2. 进购物车验证 -----
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        cart_item = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "inventory_item_name"))
        )
        assert cart_item.text == product_name
        print(f"2. 购物车验证通过: {cart_item.text}")

        # ----- 3. 结账 -----
        driver.find_element(By.ID, "checkout").click()
        driver.find_element(By.ID, "first-name").send_keys("张")
        driver.find_element(By.ID, "last-name").send_keys("三")
        driver.find_element(By.ID, "postal-code").send_keys("100000")
        driver.find_element(By.ID, "continue").click()
        print("3. 收货信息已填写")

        # ----- 4. 完成订单 -----
        driver.find_element(By.ID, "finish").click()
        complete_header = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "complete-header"))
        )
        assert "Thank you" in complete_header.text
        print(f"4. 订单完成: {complete_header.text}")