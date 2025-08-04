import requests


class CFUser:
    def __init__(self, handle):
        self.handle = handle
        self.submissions = []

        self.accepted = []
        self.accepted_unique = 0
        self.attempted_unique = 0

        self.avg_accepted_rating = 0
        self.max_accepted_rating = 0
        self.avg_attempted_rating = 0
        self.max_attempted_rating = 0

        self.tags = {}
        self.language_used = {}

        self.__language_map = {
            'py': "Python",
            'c++': "C++",
            'java': "Java",
            'gnu c': 'C',
            'javascript': "Javascript"
        }

        self.__metrics = {}

    def fetch_submissions(self):
        url = f"https://codeforces.com/api/user.status"
        params = {
            "handle": self.handle,
            "from": 1,
            "count": 9999
        }

        try:
            response = requests.get(url, params=params)
            data = response.json()

            if data["status"] == "OK":
                self.submissions = data["result"]
            else:
                return f"Error for {self.handle}: {data.get('comment')}"
        except requests.exceptions.RequestException as e:
            return f"Error for {self.handle}: {e}"
        return None

    def process_accepted(self):
        count = 0
        rating = 0
        accepted = set()
        for sub in self.submissions:
            if sub['verdict'] == 'OK':
                if sub['problem']['name'] not in accepted:
                    count += 1
                    accepted.add(sub['problem']['name'])
                    self.accepted.append(sub)
                    try:
                        rating += sub['problem']['rating']
                        if sub['problem']['rating'] > self.max_accepted_rating:
                            self.max_accepted_rating = sub['problem']['rating']
                    except KeyError:
                        if count > 0:
                            avg_rating = rating / count
                            rating += avg_rating
                            if avg_rating > self.max_accepted_rating:
                                self.max_accepted_rating = avg_rating

        if count > 0:
            self.avg_accepted_rating = rating / count
        self.accepted_unique = count

    def process_attempted(self):
        count = 0
        rating = 0
        attempted = set()
        for sub in self.submissions:
            if sub['problem']['name'] not in attempted:
                count += 1
                attempted.add(sub['problem']['name'])
                try:
                    rating += sub['problem']['rating']
                    if sub['problem']['rating'] > self.max_attempted_rating:
                        self.max_attempted_rating = sub['problem']['rating']
                except KeyError:
                    if count > 0:
                        avg_rating = rating / count
                        rating += avg_rating
                        if avg_rating > self.max_attempted_rating:
                            self.max_attempted_rating = avg_rating

        if count > 0:
            self.avg_attempted_rating = rating / count
        self.attempted_unique = count

    def count_tags(self):
        for sub in self.accepted:
            for x in sub['problem']['tags']:
                try:
                    self.tags[x] += 1
                except KeyError:
                    self.tags[x] = 1

    def get_tags(self):
        self.count_tags()
        sorted_tags = sorted(self.tags.items(), key=lambda kv: kv[1], reverse=True)
        sorted_tags = sorted_tags[1:6]
        tags = [f"{x[0]}" for x in sorted_tags]
        return ", ".join(tags)

    def count_languages(self):
        for sub in self.accepted:
            lang = sub['programmingLanguage'].lower()
            lang_map = self.get_lang_map()
            for k, v in lang_map.items():
                if k in lang:
                    lang = v
            try:
                self.language_used[lang] += 1
            except KeyError:
                self.language_used[lang] = 1

    def get_lang_map(self):
        return self.__language_map

    def get_lang_used(self):
        self.count_languages()
        sorted_langs = sorted(self.language_used.items(), key=lambda kv: kv[1], reverse=True)
        return ", ".join([f"{lang} ({count})" for lang, count in sorted_langs])

    def populate_metrics(self):
        error = self.fetch_submissions()
        if error:
            return error
        self.process_accepted()
        self.process_attempted()
        self.__metrics['User'] = self.handle
        self.__metrics['Total Solved'] = self.accepted_unique
        self.__metrics['Total Attempted'] = self.attempted_unique
        self.__metrics['Average Problem Rating (solved)'] = round(self.avg_accepted_rating)
        self.__metrics['Max Problem Rating (solved)'] = self.max_accepted_rating
        self.__metrics['Average Problem Rating (attempted)'] = round(self.avg_attempted_rating)
        self.__metrics['Max Problem Rating (attempted)'] = self.max_attempted_rating
        self.__metrics['Top Problem Tags'] = self.get_tags()
        self.__metrics['Language Used'] = self.get_lang_used()
        return None

    def get_metrics(self):
        error = self.populate_metrics()
        if error:
            return error
        return self.__metrics
