class TemplateBuilder:
    
    def build(self,template_str:str)->dict:
        lines = template_str.splitlines()
        questions = dict()
        for line in lines:
            if self.__has_question(line):
                questions[self.__get_question_text(line)]=line
        return questions
    
    def __has_question(self,text:str)->bool:
        return text.find("${")>=0 and text.find("}")>=0
    
    def __get_question_text(self,text:str)->str:
        return text[text.index("${"):text.index("}")+1]
    