# -*- coding: utf-8 -*-
import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.adapters.listadapter import ListAdapter
from kivy.uix.listview import ListItemButton, ListView, ListItemLabel
from kivy.clock import Clock
import cPickle as pk
import random, time 


Builder.load_string('''
<Widget>:
    font_name: 'DroidSansFallback.ttf'# solve Chinses display issue
<ListItemButton>:
    deselected_color: 1,1,1,1
    selected_color: 0,0,0,1
    #~ text_size: self.width, None
    #~ size_hint_y: None # height will not be automatically resized by anything
    #~ height: self.texture_size[1]*2 # set height to be sufficient to display all text
<OneViewer@BoxLayout>:
    orientation: 'vertical'
    article_panel: article_panel
    title_label: title_label
    srcn_manager: srcn_manager
    ActionBar:
        pos_hint: {'top':1}
        ActionView:
            use_separator: True
            ActionPrevious:
                id: title_label
                title: 'ONE'
                with_previous: srcn_manager.current == 's2' # boolean
                on_release: srcn_manager.current = 's1'
            ActionOverflow:
            ActionButton:
                text: 'Star'
                disabled: srcn_manager.current == 's1' # boolean
                icon: '/home/wx/Dropbox/OC/KIVY/OneArticle/star_0.png'
            ActionButton:
                text: 'Random'
                on_press: root.random_article()
            ActionButton:
                text: 'Prev'
                disabled: srcn_manager.current == 's1' # boolean
                on_press: root.prev_article()
            ActionButton:
                text: 'Next'
                disabled: srcn_manager.current == 's1' # boolean
                on_press: root.next_article()

    ScreenManager:
        id: srcn_manager
        on_current: root.on_change_screen()
        Screen:
            name: 's1'
            ListView:
                adapter: root.list_adapter
        Screen:
            name: 's2'
            ScrollView: 
                RstDocument:
                    id: article_panel
                    font_size: 25
                    text: 'hello world'*100
''')


ONE = pk.load(open('one.dict','rb'))
VOLS = sorted( ONE.keys() )
TITLES = ['VOL. %d %s %s'%(vol, ONE[vol]['title'], ONE[vol]['author']) for vol in VOLS]



class OneViewer(BoxLayout):
    article_panel = ObjectProperty()
    title_label = ObjectProperty()
    srcn_manager = ObjectProperty()
    list_adapter = ListAdapter(data=TITLES,
                           args_converter=lambda row_index, obj: {'text': obj,
                                         'size_hint_y': None, 'height': 30}, #, 'size_hint_x': None, 'pos_x':root.center[0]
                           cls=ListItemButton,
                           selection_mode='single',
                           allow_empty_selection=True)
    art = None
    
    #~ def __init__(self):
        #~ print 'hello'
        
    def load_article(self, art):
        #~ self.article_panel.font_name = kivy.resources.resource_find("DroidSansFallback.ttf")
        self.art = art
        ctt, tt, aut = art['content'], art['title'], art['author']
        txt = '%s\n-------------------------------\n**%s**\n\n%s'%(tt,aut,ctt.replace('\n','\n\n'))
        self.article_panel.text = txt
        self.title_label.title = str(art['vol'])+'. '+art['title']+' '+art['author']
        self.srcn_manager.current = 's2'
    
    def on_change_screen(self,*args):
        if self.srcn_manager.current=='s1':
            self.title_label.title = 'ONE'
    
    def random_article(self):
        vol = random.choice(ONE.keys())
        art = ONE[vol]
        self.load_article(art)
    
    def prev_article(self):
        vol = self.art['vol']
        while vol>=1:
            vol-=1
            if vol in ONE.keys(): break
        art = ONE[vol]
        self.load_article(art)
        
    def next_article(self):
        vol = self.art['vol']
        while vol<=930:
            vol+=1
            if vol in ONE.keys(): break
        art = ONE[vol]
        self.load_article(art)


class OneArticleApp(App):
    ov = ObjectProperty()
    
    def on_item_select(self,adp,*args):
        if len(adp.selection)==0:
            return
        item = adp.selection[0]
        item.deselect()
        vol = int( item.text.split()[1] )
        Clock.schedule_once(lambda dt: self.ov.load_article(ONE[vol]), .01)
        
                

    def build(self):
        self.ov = OneViewer()
        self.ov.list_adapter.bind(on_selection_change=self.on_item_select)
        return self.ov
        

OneArticleApp().run()
