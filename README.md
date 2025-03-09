# NoTime4Hilan
## conf.json
  This file is the way to fill your information so the program will be able to sign in to your account.<br>
  In addition there are plenty of hooks you can use to costumize its way of working.
  
  ### Required Information
  #### website
    The adderss of the site's login page.
    
    Example: "https://nvidia.net.hilan.co.il/login"
  #### username
    The login user name of the employee. 
    It should be the employee's worker ID.
    
    Example: "03245"
  #### password
    The login password of the employee.
    
    Example: "YaiRHamelecHShyaa!!a"
  
  ### Optional Information
  #### is_last_month
    If set to True, the program will fill the information of last month instead of the current one.
    
    default: "False"
    
    Example: "True"
  #### presence
    After choosing a day to fill, you should select which kind of work you did.
    This value should be a number that represents the choice.
    
    default: "0"
    
    Examples: "0" (presence)
          "15" (w. home)

    Guide: To find this number, you should go to Hilan, select any day to fill, and inspect the select button.
           To inspect it you might "right_click->inspect" or use "ctrl+shift+c" and click the select button.
           In the source code that opens, find the value attribute under the <option> block you seek.
  #### start_time
    The time you start working every day.

    Default: "09:00:

    Example: "09:30"
  #### min_hours
    The minimum hours you work a day. 
    Every day will be filled with at least this amount of hours.

    default: "9"

    Example: "9.5"
  #### project_code
    When filling the information of a workday, the project you work on is needed.
    This field should only concist the project number!

    default: ""

    Example: "69146"
  #### is_random
    If set to True, randomization of the hours set every day will apply.
    The randomization will be determined by "start_time_distribution" and "hours_distribution" parameters.

    default: "True"

    Example: "False"
  #### start_time_distribution
    A list that represents the distribution of the variation in start_time.
    The steps are 0.5 hour and function as described in the guide below.
  
    default: "[0.2,0.6,0.2]"
    
    Example: "[0.2, 0.5, 0.2, 0.1]"
    
    Guide: The vector could containe an even or odd number of values.
           The time set in start_time will be skewed by steps of 0.5 hours backwards or forward in time.
           
           In the odd case, the middle value will represent the odds for no change in start_time and each
           value to the left and to the right of it represents the odds to set half an hour earlier or later respectively.
           For example if "start_time" = "09:30", the vector [0.1, 0.2, 0.2, 0.3, 0.2] will correspond to [08:30, 09:00, 09:30, 10:00, 10:30].
           
           The even case would be the same with one less option of moving half an hour back.
           For example if "start_time" = "09:30", the vector [0.1, 0.4, 0.3, 0.2] will correspond to [09:00, 09:30, 10:00, 10:30].
           
  #### hours_distribution
     list that represents the distribution of the variation in min_hours.
     The steps are 0.5 hour and function as described in the guide below.

     default: "[0.8, 0.1, 0.1]"

     Example: "[0.6, 0.2, 0.1, 0.1]":

     Guide: The first value corresponds to no change in the number of hours.
            Each value to the right of it represents 0.5 hours more.
            
            For example, if "min_hours" = "9", the vector [0.6, 0.2, 0.1, 0.1] corresponds to [9, 9.5, 10, 10.5].
## NoTime4Hilan.py
  Parsing the conf file and calls functions that perform all the steps from logging in to saving the set time.
## login.py
  Handles the login page.
  Logging in and move to Hilan's home page.
## navigate.py
  The sole purpose of this file is to navigate from the home page to the page where you fill your hours.
## filler.py
  This file handles the hours filling page.
  It does 2 main actions, selecting the dates in the calendar and filling the info of the selected dates.
  Holidays and weekends (Fridays and Saturdays) are ignored. 
