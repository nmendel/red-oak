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
        status = self.info['requester_received_pizza']
        print(text + ' ' + str(status))


    def score_request_length(self):
        #After testing, 400 seemed to be a good value for max length. While there are a few posts with much higher
        #word counts, they appear to be outliers
        max_length = 400
        text = self.info['request_text']
        text_words = text.lower().split()

        #Count words in title to add to total text
        title_text = self.info['request_title']
        num_title_words = len(title_text.lower().split())
        num_words = len(text_words)
        total_words = num_words + num_title_words
        score = float(total_words)/max_length

        #return score with an upper bound of 1
        return min(score, 1)


    def score_narrative(self):
        text = self.info['request_text']
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
        total = student + money + job + family + desire

        if total > 0:
            nar = {'student': (float(student)/total), 'money': (float(money)/total), 'job': (float(job)/total),
                   'family': (float(family)/total), 'desire': (float(desire)/total)}
        else:
            nar = {'student': 0, 'money': 0, 'job': 0,
                   'family': 0, 'desire': 0}
        #narrative = max(nar, key=nar.get)
        #return self.NARRATIVES[narrative]
        return nar
  
  
    def score_requester_days_since_first_post_on_raop_at_request(self):
        #most data seemed to be 0, maximum I saw was in the hundreds place
       days= self.info['requester_days_since_first_post_on_raop_at_request']
       if(days < 999):
          return days/1000
       else:
          return 1
    
    
    def score_requester_account_age_in_days_at_request(self):
      #most data I saw was in the hundreds place, only a few that were over 1000
    	days= self.info['requester_account_age_in_days_at_request']
    	if(days < 999):
          return days/1000
    	else:
          return 1
  
          
              
