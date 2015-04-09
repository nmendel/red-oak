#Request Info


class RequestInfo():
    NARRATIVES = {'student': .232, 'money': .323,
                  'job': .319,'family': .235,'desire': .17}
    STUDENT = ['college', 'student', 'university', 'finals', 'study',
               'studying', 'class', 'semester', 'school', 'roommate', 'project',
               'tuition', 'dorm']
    MONEY = ['money', 'bill', 'bills', 'rent', 'bank', 'account', 'paycheck',
             'due','broke','bills','deposit','cash','dollar','dollars','bucks','paid','payed','buy',
             'check','spent','financial','poor','loan','credit','budget','day','now','time','week',
             'until','last','month','tonight','today','next','night','when','tomorrow','first','after',
             'while','before','long','hour','Friday','ago','still','due','past','soon','current','years',
             'never','till','yesterday','morning','evening']
    JOB = ['job','unemployment','employment','hire','hired','fired','interview','work','paycheck']
    FAMILY = ['husband','wife','family','parent','parents','mother','father','mom','mum','son','dad','daughter']
    DESIRE = ['friend','party','birthday','boyfriend','girlfriend','date','drinks','drunk','wasted','invite',
              'invited','celebrate','celebrating','game','games','movie','beer','crave','craving']

    def __init__(self, request_data):
        self.info = request_data

    def print_request(self):
        text = self.info['request_text']
        status = self.info.get('requester_received_pizza', '')
        print(text + ' ' + str(status))


    def score_request_length(self):
        #After testing, 400 seemed to be a good value for max length. While there are a few posts with much higher
        #word counts, they appear to be outliers
        max_length = 400
        text = self.info.get('request_text', self.info.get('request_text_edit_aware', ''))
        text_words = text.lower().split()

        #Count words in title to add to total text
        title_text = self.info['request_title']
        num_title_words = len(title_text.lower().split())
        num_words = len(text_words)
        total_words = num_words + num_title_words
        score = round(float(total_words)/max_length, 2)

        #return score with an upper bound of 1
        return min(score, 1)


    def score_narrative(self):
        text = self.info.get('request_text', self.info.get('request_text_edit_aware', ''))
        words = text.lower().split()

        student = 0
        for lex in self.STUDENT:
            for word in words:
                if lex == word:
                    student += 1

        money = 0
        for lex in self.MONEY:
            for word in words:
                if lex == word:
                    money += 1

        job = 0
        for lex in self.JOB:
            for word in words:
                if lex == word:
                    job += 1

        family = 0
        for lex in self.FAMILY:
            for word in words:
                if lex == word:
                    family += 1

        desire = 0
        for lex in self.DESIRE:
            for word in words:
                if lex == word:
                    desire += 1
        #[1, 2, 3, 4, 1, 4, 1].count(1)
        total = float(student + money + job + family + desire)
		
        def getScore(categoryScore):
            return round(categoryScore/total, 2)
 
        if total > 0:
            nar = {'student': getScore(student), 'money': getScore(money), 'job': getScore(job),
                   'family': getScore(family), 'desire': getScore(desire)}
        else:
            nar = {'student': 0, 'money': 0, 'job': 0,
                   'family': 0, 'desire': 0}
        #narrative = max(nar, key=nar.get)
        #return self.NARRATIVES[narrative]
        return nar
  
  
    def score_requester_days_since_first_post_on_raop_at_request(self):
        #most data seemed to be 0, maximum I saw was in the hundreds place
       days= self.info['requester_days_since_first_post_on_raop_at_request']
       if(days < 1000):
          return round(days/float(1000), 2)
       else:
          return 1
    
    
    def score_requester_account_age_in_days_at_request(self):
      #most data I saw was in the hundreds place, only a few that were over 1000
    	days= self.info['requester_account_age_in_days_at_request']
    	if(days < 1000):
          return round(days/float(1000), 2)
    	else:
          return 1
  
    def score_requester_account_age_in_days_at_retrieval(self):
      #most data I saw was in the hundreds place, only a few that were over 1000
    	days= self.info['requester_account_age_in_days_at_retrieval']
    	if(days < 1000):
          return round(days/float(1000), 2)
    	else:
          return 1
            
    def score_requester_upvotes_minus_downvotes_at_request(self):
      #most data I saw was in the hundreds place, but a handful were in the thousands, picked 4000 as the upper limit but this can be changed
    	votes= self.info['requester_upvotes_minus_downvotes_at_request']
    	if(votes< 4000):
          return round(days/float(4000), 2)
    	else:
          return 1
          
    def score_requester_upvotes_minus_downvotes_at_retrieval(self):
      #most data I saw was in the hundreds place, but a handful were in the thousands, picked 4000 as the upper limit but this can be changed
    	votes= self.info['requester_upvotes_minus_downvotes_at_retrieval']
    	if(votes< 4000):
          return round(days/float(4000), 2)
    	else:
          return 1
          
    def score_requester_upvotes_plus_downvotes_at_request(self):
      #most data I saw was in the hundreds place, but some were in the thousands, picked 10000 as the upper limit but this can be changed
    	votes= self.info['requester_upvotes_plus_downvotes_at_request']
    	if(votes< 10000):
          return round(days/float(10000), 2)
    	else:
          return 1
          
    def score_requester_upvotes_plus_downvotes_at_retrieval(self):
      #most data I saw was in the hundreds place, but some were in the thousands, picked 10000 as the upper limit but this can be changed
    	votes= self.info['requester_upvotes_plus_downvotes_at_retrieval']
    	if(votes< 10000):
          return round(days/float(10000), 2)
    	else:
          return 1          
          
    def score_post_was_edited(self):
      #boolean value so returns either 0 or 1
    	edited= self.info['post_was_edited']
    	if(edited==1):
          return 1
    	else:
          return 0

    def score_requester_number_of_comments_at_request(self):
      #most data I saw was below 100 but a handful were in the hundreds, picked 500 as the upper limit but this can be changed
    	comments= self.info['requester_number_of_comments_at_request']
    	if(comments<500):
          return round(days/float(500), 2)
    	else:
          return 1
          
    def score_requester_number_of_comments_at_retrieval(self):
      #most data I saw was in the hundreds picked 1000 as the upper limit but this can be changed
    	comments= self.info['requester_number_of_comments_at_retrieval']
    	if(comments<1000):
          return round(days/float(1000), 2)
    	else:
          return 1  
          
    def score_requester_number_of_posts_at_request(self):
      #most data I saw was below 100 with a few going over 100, picked 100 as upper limit but this can be changed
    	posts= self.info['requester_number_of_posts_at_request']
    	if(posts<100):
          return round(days/float(100), 2)
    	else:
          return 1 
          
    def score_requester_number_of_posts_at_retrieval(self):
      #most data I saw was below 100 with some going over 100, picked 200 as upper limit but this can be changed
    	posts= self.info['requester_number_of_posts_at_retrieval']
    	if(posts<200):
          return round(days/float(200), 2)
    	else:
          return 1
          
    def score_requester_number_of_subreddits_at_request(self):
        # A small percentage have a whole bunch, but most have only a handful.
        # 50 seems like a reasonable max
        num = self.info['requester_number_of_subreddits_at_request']
        return min(round(num / float(50), 2), 1.0)
        
    def score_requester_user_flair(self):
        # This is an icon or something, so its either something or nothing
        flair = self.info['requester_user_flair']
        return not (flair == 'null' or flair == None or flair == '')
        
    def score_requester_number_of_comments_in_raop_at_request(self):
        #usually very low 0 or 1, small amount have above this
        comments = self.info['requester_number_of_comments_in_raop_at_request']
        if(comments<10):
          return round(days/float(10), 2)
        else:
          return 1

    def score_requester_number_of_comments_in_raop_at_retrieval(self):
        #usually a little more than request, small amount continue to comment on raop
        comments = self.info['requester_number_of_comments_in_raop_at_retrieval']
        if(comments<30):
          return round(days/float(30), 2)
        else:
          return 1