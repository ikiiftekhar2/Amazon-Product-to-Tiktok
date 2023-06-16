from keys import affiliate_tag

def convert_to_affiliate_link(product_link):
    if "amazon.ca" not in product_link:
        print("Invalid Amazon product link.")
        return None

    affiliate_link = product_link.split("/dp/")[0] + "/dp/" + product_link.split("/dp/")[1].split("/")[0] + "/?tag=" + affiliate_tag
    return affiliate_link