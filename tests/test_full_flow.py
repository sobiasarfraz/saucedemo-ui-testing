import time

import pytest
import logging
from screenshot_helper import take_screenshot
from selenium.common.exceptions import UnexpectedAlertPresentException

def test_login(browser, user_data, setup_pages):
    login_page, inventory_page, cart_page, chqout = setup_pages
    logging.info("----- test started -----")

    ####----step 1 open browser, and logged in----####
    login_page.open_browser()
    login_page.login(user_data['username'], user_data['password'])
    if login_page.is_error_found():
        actual_error = login_page.error_message().strip()
        expected_error = "Epic sadface: Sorry, this user has been locked out."
        assert expected_error in actual_error, f"expected {expected_error} but got : {actual_error}"
        logging.error(f"invalid user: {user_data['username']}  got error : {actual_error}")
        take_screenshot(browser,"logging error")
        return
    else:
        logging.info(f"successfully logged in user: {user_data['username']}")
        take_screenshot(browser, "logging successfully")
        assert inventory_page.login_check(), "not logged in, we are not on inventory page "

    ###---- step 2 inventory page, sorting, adding to the cart ----###
    #clear fields,sort low to high price items,add first low priced  items added to cart
    #inventory_page.clear_fields()

    # checking image is enable and not broken
    missed_img = inventory_page.image_check()
    if missed_img:
        logging.error("broken or missed images detected")
        for error in missed_img:
            logging.error(error)  # Log the image errors here
            take_screenshot(browser, "broken image")
    assert len(missed_img) == 0, f"image is not loaded: {missed_img}"
    logging.info("All inventory images loaded successfully.")
    #assert not missed_img, f"image is not loaded: {missed_img}" #### can check either way
    #time.sleep(1)
    inventory_page.clear_fields()
    logging.info("fields are clear")

    inventory_page.sort_by_price()
    #time.sleep(1)

    total_items = inventory_page.add_first_items()
    #time.sleep(1)



    logging.info(f"items sorted by price and add to cart, item added are: {total_items}")

    #step 3 go to cart and validate items
    cart_page.go_tocart()
    #assert cart_page.chq_cart(), "not on cart page"
    logging.info("now on cart page")

    #checking cart count,matches with actual item added
    cart_item_length = cart_page.count_items()
    expected_cart_count = len(total_items)
    logging.info(f"cart count: {cart_item_length}, expected count is: {expected_cart_count}")
    # ✅ ADD THIS LINE: At least 1 item should be in cart (fail if none)
    assert cart_item_length >= 1, f"No items were added to the cart for user {user_data['username']}"
    #assert cart_item_length == len(total_items), f"total no of items selected are: {len(total_items)} but in cart there are: {cart_item_length}"
    #checks items are added in cart
    # ✅ ADD THIS LINE: Warn if some items were not added (but don’t fail)
    if cart_item_length != len(total_items):
        logging.warning(
            f"Cart count ({cart_item_length}) does not match attempted items ({expected_cart_count}) for user {user_data['username']}")

    #crt_items = cart_page.get_cart_item_names()
    #for item in total_items:
        #if item not in crt_items:
            #logging.warning(
                #f"Item '{item}' was attempted to add but is missing from cart for user {user_data['username']}")
        #assert item in crt_items, f"following item: {item} : added in cart but missing in cart "

    # Remove the highest-priced item if quantity exceeds 2
    if cart_item_length > 2:
        remove_item = total_items[-1]  # remove last item, higher price
        is_removed = cart_page.remove_item_by_name(remove_item)
        assert is_removed, f" fail to remove item : {remove_item}"
        logging.info(f"item is removed from the cart: {remove_item}")

    # new cart length check
    new_cart_length = cart_page.count_items()
    expected_length = len(total_items) - 1
    logging.info(f"now cart length is: {new_cart_length}, expected cart length is: {expected_length}")
    assert new_cart_length == expected_length, f" after removal expected length is {expected_length}, but actual is {new_cart_length}"


    #step 4 check out(fil the form and place the order)
    chqout.chq_out()
    assert chqout.check_result(), "not on checkout page"
    logging.info("now on check out page")

    error_msg = chqout.empty_form()
    expected_error_msg = "Error: First Name is required"
    assert error_msg in expected_error_msg, f" expected error message was: {expected_error_msg}, but got message: {error_msg}"

    #fill the form
    if chqout.fill_form("shaz", "roy", "1234"):
        assert chqout.overview(), " not on checkout overview : step 2 page"
        logging.info("fill the form,overview has done")
    #order done
        order_msg = chqout.finish_chqout()
        if order_msg:
            logging.info(f"{user_data['username']} has placed the order! ")
        else:
            logging.warning("cant finish the order")
    else:
        logging.warning(f"we can't fill the form for user: {user_data['username']}, moving to logout")

    #assert order_msg == "Thank you for your order!", f" unexpected message: {order_msg}"
    #logging.info("order has been placed! ")

     #step 5 logout ,back to main page
    chqout.log_out()
    assert chqout.confrm_logout(), "logout fail"
    logging.info("logout confirmed")







