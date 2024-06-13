1. DESCRIPTION
2. HOW TO USE
3. WHAT I LEARNED
________________________________________

## 1. DESCRIPTION
  Second project using Django framework.
  
  Project is a simple social-app.
  It contains dynamic content with images, all CRUD functionalities and searching field. Data is stored in simple sqlite database for easier use.

  There are:
  -main page with posts of people that you follow
  -user profile page, 
  -user post page, 
  -liking and commenting posts functionallities
  -possibility following and unfollowing user
  -searching users
  
  Hardest thing in this project for me was liking posts and dynamically display gray or blue button depending on whether currently logged in user liked specific post or not.
  I decided to create 'Like' model which has foreign key to post and user that clicked like button. 
  Next I wrote code in views.py that puts all posts logged user liked to list and passes it to template.
  Finally, in template, for every post that is displaying in loop, my code checks if this post is in this list mentioned above.
  
  

## 2. HOW TO USE
   
   2.1 WEB PAGE
     - You should have python 3.11.4 and pip 23.1.2 installed on your device
     - Then install all libraries using 'pip install -r installed_packages.txt' in terminal from project main directory
     - You can run server locally from main directory using command 'python manage.py runserver'
     - There is allready one user (superuser): admin with password "1"
      
## 3. WHAT I LEARNED 

    Learned how to input images to project, connect it's localization into database and let project user upload it.
    Also I had more things to accomplish i think and operation logics were harder than in previous projects.
