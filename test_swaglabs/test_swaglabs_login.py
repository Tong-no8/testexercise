import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


# ========== 登录测试数据 ==========
login_test_data = [
    # (用户名, 密码, 是否应该成功, 场景)
    ("standard_user", "secret_sauce", True, "正常登录"),
    ("locked_out_user", "secret_sauce", False, "被锁定的账号"),
    ("standard_user", "wrong_password", False, "密码错误"),
    ("", "secret_sauce", False, "用户名为空"),
    ("standard_user", "", False, "密码为空"),
]


# ========== 夹具 ==========
@pytest.fixture
def driver():
    """启动浏览器，测试结束后关闭"""
    print("\n[前置] 启动浏览器...")
    service = Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=service)
    browser.implicitly_wait(5)
    browser.maximize_window()
    yield browser
    print("\n[后置] 关闭浏览器...")
    browser.quit()


# ========== 测试类 ==========
class TestSwagLabsLogin:
    """Swag Labs 登录模块测试"""

    BASE_URL = "https://www.saucedemo.com"

    @pytest.mark.parametrize("username,password,should_succeed,test_scene", login_test_data)
    def test_login_scenarios(self, driver, username, password, should_succeed, test_scene):
        """
        登录参数化测试：覆盖正常登录、锁定账号、密码错误、空用户名、空密码
        """
        # 1. 打开登录页
        driver.get(self.BASE_URL)

        # 2. 找到用户名和密码输入框，填入数据
        wait = WebDriverWait(driver, 10)
        username_input = wait.until(
            EC.presence_of_element_located((By.ID, "user-name"))
        )
        password_input = driver.find_element(By.ID, "password")
        login_button = driver.find_element(By.ID, "login-button")

        username_input.clear()
        password_input.clear()

        # 输入（没传用户名或密码就不填）
        if username:
            username_input.send_keys(username)
        if password:
            password_input.send_keys(password)

        # 3. 点击登录
        login_button.click()

        # 4. 根据预期判断结果
        if should_succeed:
            # 成功：应该跳转到商品列表页
            assert "inventory" in driver.current_url.lower()
            print(f"✅ [{test_scene}] 登录成功，已跳转到商品列表页")
        else:
            # 失败：应该出现错误提示
            error_element = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-test="error"]'))
            )
            assert error_element.is_displayed()
            print(f"✅ [{test_scene}] 登录失败，错误提示已显示")