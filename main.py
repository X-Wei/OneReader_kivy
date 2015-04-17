# -*- coding: utf-8 -*-
import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.properties import ObjectProperty
import cPickle as pk
import random 


Builder.load_string('''
<Widget>:
    font_name: 'DroidSansFallback.ttf'
    
<OneViewer@BoxLayout>:
    
    orientation: 'vertical'
    article_panel: article_panel
    title_label: title_label
    ActionBar:
        pos_hint: {'top':1}
        ActionView:
            use_separator: True
            ActionPrevious:
                id: title_label
                title: 'Article title'
                with_previous: False
            ActionOverflow:
            ActionButton:
                text: 'Btn0'
                icon: 'star_0.png'
            ActionButton:
                text: 'Btn1'
            ActionButton:
                text: 'Btn2'
            ActionButton:
                text: 'Btn3'
            ActionButton:
                text: 'Btn4'
            ActionGroup:
                text: 'Group1'
                ActionButton:
                    text: 'Random'
                    on_press: root.random_article()
                ActionButton:
                    text: 'Author'
                ActionButton:
                    text: 'Btn7'
    ScrollView: 
        RstDocument:
            id: article_panel
            font_size: 25
    

''')


one = pk.load(open('one.dict','rb'))

class OneViewer(BoxLayout):
    article_panel = ObjectProperty()
    title_label = ObjectProperty()
    
    def load_article(self, art):
        ctt = art['content']
        tt = art['title']
        aut = art['author']
        txt = '%s\n-------------------------------\n**%s**\n\n%s'%(tt,aut,ctt.replace('\n','\n\n'))
        self.article_panel.text = txt
        self.title_label.title = str(art['vol'])+'. '+tt
    
    def random_article(self):
        vol = random.choice(one.keys())
        art = one[vol]
        self.load_article(art)


class OneArticleApp(App):
    ov = ObjectProperty()
    
    def build(self):
        self.ov = OneViewer()
        self.ov.random_article()
        return self.ov
        

OneArticleApp().run()
