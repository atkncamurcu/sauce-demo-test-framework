def attach_screenshot(driver, name="screenshot"):
    import allure
    allure.attach(driver.get_screenshot_as_png(), name=name, attachment_type=allure.attachment_type.PNG)
