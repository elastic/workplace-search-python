"""Script which sets up a Custom API Source in Workplace Search and
indexes some documents under that source"""

import time
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from elastic_workplace_search import Client as WorkplaceSearch


def wait_and_click(driver: WebDriver, link_text=None, id=None, xpath=None):
    if link_text is not None:
        elem = driver.find_element_by_link_text(link_text)
    elif id is not None:
        elem = driver.find_element_by_id(id)
    elif xpath is not None:
        elem = driver.find_element_by_xpath(xpath)
    else:
        raise ValueError("element query not given")

    # Scroll to the element so it's on screen before clicking.
    driver.execute_script("arguments[0].scrollIntoView();", elem)
    elem.click()


def setup_custom_source(driver: WebDriver, username, password):
    driver.implicitly_wait(5)
    driver.get("http://localhost:8080")

    # After first time logging in the service won't display this screen.
    try:
        if driver.find_element_by_link_text("Continue to Login"):
            wait_and_click(driver, link_text="Continue to Login")
    except Exception:
        pass

    # Login with username and password
    elem = driver.find_element_by_id("email")
    elem.send_keys(username)
    elem = driver.find_element_by_id("password")
    elem.send_keys(password)

    wait_and_click(driver, xpath="//*[@data-test-subj='LoginButton']")
    wait_and_click(driver, link_text="Launch Workplace Search")

    # Create the Custom API Source
    try:
        wait_and_click(driver, link_text="Add sources")
    except Exception:
        # The source already exists so delete the old one first.
        wait_and_click(driver, link_text="Add more sources")
        wait_and_click(driver, link_text="Details")
        wait_and_click(driver, link_text="Source Settings")
        wait_and_click(driver, xpath="//*[@data-test-subj='DeleteSourceButton']")
        wait_and_click(driver, xpath="//*[@data-test-subj='confirmModalConfirmButton']")

    # Now we're on the 'Create API Source' screen, create a custom source
    wait_and_click(driver, link_text="Custom API Source")

    elem = driver.find_element_by_xpath("//*[@name='source-name']")
    elem.send_keys("custom-content-source")
    wait_and_click(driver, xpath="//*[contains(text(),'Create Custom API Source')]")

    # Show the Access Token and Key
    for elem in driver.find_elements_by_xpath("//*[@aria-label='Show credential']"):
        # Scroll to the element so it's on screen before clicking.
        driver.execute_script("arguments[0].scrollIntoView();", elem)
        elem.click()

    values = []
    for elem in driver.find_elements_by_class_name("euiFieldText"):
        values.append(elem.get_attribute("value"))
    return tuple(values[:2])


def index_documents(content_source_key, access_token):
    ws = WorkplaceSearch(
        base_url="http://localhost:8080/api/ws/v1",
        authorization_token=access_token
    )

    # Create the documents to be indexed.
    documents = []
    meals = ["sandwiches", "wraps", "smoothies", "salads"]
    for doc_id in range(51):
        meal = meals[doc_id % len(meals)]
        documents.append({
            "id": str(doc_id),
            "title": "How to prepare %s in %d steps!" % (meal, doc_id),
            "content": "Preparing %s is so easy I don't have to say much." % meal,
            "url": "https://example.com/%d/%s" % (doc_id, meals)
        })

    # Index all documents
    ws.documents.index_documents(
        content_source_key,
        documents=documents
    )


def main():
    driver = None
    try:
        try:
            options = webdriver.ChromeOptions()
            options.headless = True
            driver = webdriver.Chrome(options=options)
        except Exception:
            options = webdriver.FirefoxOptions()
            options.headless = True
            driver = webdriver.Firefox(options=options)

        # Setup a Custom Source with a given ID
        access_token, content_source_key = setup_custom_source(
            driver, username="enterprise_search", password="itsnotcloudsearch"
        )

        # Index some documents and permissions
        index_documents(content_source_key, access_token)

        print("%s:%s" % (content_source_key, access_token))
    finally:
        if driver:
            driver.quit()


if __name__ == "__main__":
    main()
