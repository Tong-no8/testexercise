import requests
import pytest

URL = "http://httpbin.org/post"

class TestLogin:
    """登录接口测试用例"""
    

    def test_login_success(self):
        payload = {"username": "admin", "password": "123456"}
        r = requests.post(URL, data=payload)
        assert r.status_code == 200
        assert r.json()['form']['username'] == "admin"
        print("正常登录用例通过")

    def test_login_no_password(self):
        payload = {"username": "admin", "password": ""}
        r = requests.post(URL, data=payload)
        assert r.status_code == 200
        assert r.json()['form']['password'] == ""
        print("密码为空用例通过")

    def test_login_empty_username_and_password(self):
        """用例3：用户名和密码均为空"""
        payload = {"username": "", "password": ""}
        r = requests.post(URL, data=payload)

        assert r.status_code == 200
        assert r.json()['form']['username'] == ""
        assert r.json()['form']['password'] == ""
        print("用户名密码均为空用例通过")


    @pytest.mark.skip(reason="这是故意失败的演示用例")
    def test_login_fail_demo(self):
        """用例4：故意失败的案例，看报告如何展示"""
        payload = {"username": "admin", "password": "123456"}
        r = requests.post(URL, data=payload)

        # 故意断言返回的状态码是 404，这会失败
        assert r.status_code == 404

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--html=report.html", "--self-contained-html"])