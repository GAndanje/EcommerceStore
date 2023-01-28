- Built on Django framework this web app runs on top of SQL3 development server
- Bootstrap framework is used to render frontend css styling
- PayPal API is used to enable payments on checkout

 
# EcommerceStore
+ An E-commerce store with Django framework
+ To be hosted on AWS server
+ To be deployed using AWS Beanstalk Service
+ Static files to be stored on Amazon S3
+ Will use amazon RDS PostGreSQL database

# App Features

## Review Rating
+ Rating stars rendered with FontAwesome.
+ Shows:
    - Average rating of the product.
    - Every users review rating. 
    - Total number of reviews so far of the product.
+ The user can see all reviews of the product in this view.
+ Admin can turn on/off reviews every review.
+ Only previous purchasers of a product can review the product.
+ 
<img width="986" alt="Screenshot 2023-01-28 at 01 52 13" src="https://user-images.githubusercontent.com/77880940/215224181-d05410f4-4099-4d4c-9537-8768881f1199.png">

## User Cart
+ Can add or decrement the cart_item here.
+ Can remove entire cart_item here.
+ Items summary before checkout
+ can confirm product variations
<img width="1260" alt="Screenshot 2023-01-28 at 01 58 39" src="https://user-images.githubusercontent.com/77880940/215224205-1673fdb4-1498-4464-8216-3575d006c2b8.png">

## User Dashboard
A user can:
    + Edit their profile including profile picture
    + View their order history
    + Change their password
    + Logout
<img width="1273" alt="Screenshot 2023-01-28 at 01 57 03" src="https://user-images.githubusercontent.com/77880940/215224217-d75c6e94-0a16-4a25-b024-5d93f9162d4c.png">


## Payment View with PayPal intergration
<img width="1275" alt="Screenshot 2023-01-28 at 01 37 18" src="https://user-images.githubusercontent.com/77880940/215224223-f34b3755-22b9-42fd-967d-4a4858bb6fc4.png">


