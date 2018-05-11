#avec doubleeeeeeeeeeeeeeeeeeeeeeeeeee json
import scrapy
import json
import codecs
import re
#from scrapy_splash import SplashRequest
from ..items import SegundamanovoItem 
#import urllib.request ,  urllib.error
from scrapy.spiders import CrawlSpider

# lien au site https://www.segundamano.mx/anuncios/mexico/inmuebles
class SegundamanovomarsSpider(scrapy.Spider):
    name = 'segundamano_Avril'
    allowed_domains = ['webapi.segundamano.mx', 'segundamano.mx']
    handle_httpstatus_list = [301, 302, 502, 200]
    download_delay = 0
    download_timeout = 280

    start_urls = ['https://webapi.segundamano.mx/nga/api/v1/public/klfst?lang=es&category=2021&company_ad=1&lim=36',
    'https://webapi.segundamano.mx/nga/api/v1/public/klfst?lang=es&category=2021&company_ad=0&lim=36']
    #
    #
    def correct(self,champ):

        return str(champ).replace('\r', ' ').replace('\n', ' ').replace('\t', ' ').replace(';', ' ').replace('\"', ' ')


    #@property
    def parse(self, response):#120,840 anuncios en Venta y renta de inmuebles en México 12_02

        #en va utiliser cette comande " .decode('utf8') " car en une lecture de json avec le python 3.5 
        #si il est python 2  utilisation direct de response.body sans  le decodage car il est une str direct n est pas byte comme le python 3.5
        body_json=response.body.decode('utf8')
        data = json.loads(body_json)
        for jsonresponse in data.get('list_ads',[]):
            myItem = SegundamanovoItem()
            #myItem['SIRET'] = data.get('Result')[0].get('Sections')[1].get('Tags')[18].get('Value')
            #key = data.get('Result')[0].get('Sections')[1].get('Tags')[18].get('Key')
            try:
                myItem['ANNONCE_LINK'] = self.correct(jsonresponse.get('ad').get('share_link'))
            except:
                pass

            try:    
                ad_id = jsonresponse.get('ad').get('ad_id')
            except:
                pass

            link = myItem['ANNONCE_LINK'].split('/')
            myItem['ID_CLIENT'] = self.correct(link[-1])

            try:
                myItem['OPTIONS'] = self.correct(jsonresponse.get('ad').get('body'))
            except:
                pass

            try:
                nom = self.correct(jsonresponse.get('ad').get('subject'))
                myItem['NOM']=nom
            except:
                pass

            try:
                myItem['PHOTO'] = self.correct(len(jsonresponse.get('ad').get('images')))
            except:
                myItem['PHOTO'] = 0
            devise=""
            prix=""
            try:
                devise= self.correct(jsonresponse.get('ad').get('list_price').get('currency'))
                prix= self.correct(jsonresponse.get('ad').get('list_price').get('price_value'))

            except:
                pass
            
           # if devise=="MXN":
           #     myItem['PRIX'] =round(float(prix)/19)
           # else:
            myItem['PRIX'] =str(prix)+" "+str(devise)

            try:
                annonce_date = self.correct(jsonresponse.get('ad').get('list_time').get('label'))
            except:
                pass
#ajouter a chaque foois le mois en cour
            if annonce_date:
                if 'feb' in annonce_date:
                    cc = annonce_date.split(' ')
                    myItem['ANNONCE_DATE'] = '2018-02-'+cc[0]+' '+cc[-1]+':00'
                elif 'enero' in annonce_date:
                    cc = annonce_date.split(' ')
                    myItem['ANNONCE_DATE'] = '2018-01-'+cc[0]+' '+cc[-1]+':00'
                elif 'dic' in annonce_date:
                    cc = annonce_date.split(' ')                                                                                                               
                    myItem['ANNONCE_DATE'] = '2017-12-'+cc[0]+' '+cc[-1]+':00'
                elif 'oct' in annonce_date:
                    cc = annonce_date.split(' ')
                    myItem['ANNONCE_DATE'] = '2017-10-'+cc[0]+' '+cc[-1]+':00'
                elif 'nov' in annonce_date:
                    cc = annonce_date.split(' ')
                    myItem['ANNONCE_DATE'] = '2017-11-'+cc[0]+' '+cc[-1]+':00'
                elif 'marzo' in annonce_date:
                    cc = annonce_date.split(' ')
                    myItem['ANNONCE_DATE'] = '2018-03-'+cc[0]+' '+cc[-1]+':00'

                else:
                    myItem['ANNONCE_DATE']=annonce_date

            try:
                province = self.correct(jsonresponse.get('ad').get('locations')[0].get('label'))
                myItem['PROVINCE']=province
            except:
                pass
            try:
                ville = self.correct(jsonresponse.get('ad').get('locations')[0].get('locations')[0].get('label'))
                myItem['VILLE']=ville
            except:
                pass
            adresse_private=""
            try:
                adresse_private = self.correct(jsonresponse.get('ad').get('locations')[0].get('locations')[0].get('locations')[0].get('label'))
            except:
                pass
           # try:
           #     myItem['SELLER_TYPE'] = self.correct(jsonresponse.get('ad').get('type').get('label')) #in reality this is the ACHAT_LOCATION change it later with 1 or 2
           # except:
            #    pass
            try:
                contact =self.correct( jsonresponse.get('ad').get('user').get('account').get('name'))
            except:
                pass
#------------------------------------------Ajouter par a port le imoo 
            
            try:
                carburant =self.correct( jsonresponse.get('ad').get('ad_details').get('fuel').get('single').get('label'))
                myItem['CARBURANT']=carburant
            except:
                pass

            try:
                boite =self.correct( jsonresponse.get('ad').get('ad_details').get('gearbox').get('single').get('label'))
                myItem['BOITE']=boite

            except :
                pass

            try:

                kilometrage =self.correct( jsonresponse.get('ad').get('ad_details').get('mileage').get('single').get('code'))
                myItem['KM']=kilometrage
            except:
                pass

            try:
                annee =self.correct( jsonresponse.get('ad').get('ad_details').get('regdate').get('single').get('code'))
                myItem['ANNEE']=annee
            except:
                pass

            try:
                marque =self.correct( jsonresponse.get('ad').get('ad_details').get('vehicle_brand').get('single').get('label'))
                myItem['MARQUE']=marque
            except:
                pass

            try:
                model =self.correct( jsonresponse.get('ad').get('ad_details').get('vehicle_model').get('single').get('label'))   
                myItem['MODELE']=model
            except:
                pass
#--------------------------------------
            myItem['SITE']='segundamano'
         
            full_url_telephone = 'https://webapi.segundamano.mx/nga/api/v1/public/klfst/'+myItem['ID_CLIENT']+'/phone?lang=es' 

            url_list_json=response.url
            #print ("***",url_list_json)
            if ("company_ad=1" in str(url_list_json)):
                #profisionel Y
                myItem['TYPE']='Y'
            else:
                #particular =private = N
                myItem['TYPE']='N'
            shop_id=""
            try:
                shop_id = self.correct(jsonresponse.get('ad').get('shop_id')) #pour distinger si il es pro alors ce id existe et si il est vide alors private
            except:
                print ("not found")
            if shop_id == "None" or shop_id=="":

                myItem['CONTACT']=contact
                #-------  agence ville et agence departement est le meme que adress Ubicación 
                myItem['VILLE']=ville
                myItem['PROVINCE']=province
                myItem['ADRESSE']=adresse_private
               
                try:
                    request_adress=scrapy.Request(url=full_url_telephone,callback=self.detail_page,dont_filter=True) 
                    request_adress.meta["myItem"]=myItem
                    yield request_adress
                    #------------------------json vers les numero telephone  direct-------

                except:
                    print("error ")
            else:

                myItem['CONTACT']=contact
                myItem['GARAGE_NAME']=contact
                myItem['GARAGE_ID']=shop_id
                myItem['minisite']="https://www.segundamano.mx/tiendas/"+str(shop_id)

#------------------------------------json vers le adress agence pour prendre le code de adress agence 
#et en recherche adresse corespondant a se code dans une autre json puis extraction du numero telephone de une final requeset json 

                json_adress_agence="https://webapi.segundamano.mx/shops/api/v1/public/shops/"+str(shop_id)


                try:
                    request_adress=scrapy.Request(url=json_adress_agence,callback=self.adress_agence_code,dont_filter=True) 
                    request_adress.meta["myItem"]=myItem
                    request_adress.meta["full_url_telephone"]=full_url_telephone
                    yield request_adress
                except:
                    print("error")
                #cette request est vers le page json qui en va attraper le code de l adrresss



           
#-/*/////////////////////////Next page 
        next_id = data.get('next_page',[])
        if myItem['TYPE']=='Y':

            next_page = 'https://webapi.segundamano.mx/nga/api/v1/public/klfst?lang=es&category=2021&company_ad=1&o='+str(next_id)
        if myItem['TYPE']=='N':
            next_page = 'https://webapi.segundamano.mx/nga/api/v1/public/klfst?lang=es&category=2021&company_ad=0&o='+str(next_id)
        
        if next_page:
            req = scrapy.Request(next_page)#,  callback=self.parse)
            yield req


            
#-------------------------agence adresss code  ---------------------------------------


    def adress_agence_code(self,response):
        body_json=response.body.decode('utf8')
        data=json.loads(body_json)
        myItem=response.meta['myItem']
        full_url_telephone=response.meta['full_url_telephone']
        #try:
        
        agence_code_region=data.get('locations')[0].get('code')                               
        agence_code_municipality=data.get('locations')[0].get('locations')[0].get('code')    

        agence_code_complet="https://webapi.segundamano.mx/nga/api/v1.1/public/regions?lang=es&depth=1&from=region:"+str(agence_code_region)
    
        request_adress_complet=scrapy.Request(url=agence_code_complet,callback=self.adress_agence_complet,dont_filter=True) 
        request_adress_complet.meta["agence_code_municipality"]=str(agence_code_municipality)
        request_adress_complet.meta["agence_code_region"]=str(agence_code_region)

        request_adress_complet.meta["myItem"]=myItem
        request_adress_complet.meta["full_url_telephone"]=full_url_telephone
        print(agence_code_municipality,"  ",agence_code_region)

    
        yield request_adress_complet


# #------------------------- remplir dans item le agence adresss complet et envoi une request pour attraper le numero telephone avec meta de lien de numero  ---------------------------------------

    def adress_agence_complet(self,response):

        print("************final***************************************")

        body_json=response.body.decode('utf8')
        data=json.loads(body_json)

        myItem=response.meta['myItem']
        agence_code_municipality=response.meta["agence_code_municipality"]
        agence_code_region=response.meta["agence_code_region"]
        full_url_telephone=response.meta["full_url_telephone"]
        i=0
        #json_agence_code_region=self.correct(data.get('code'))
        #while agence_code_region != json_agence_code_region and agence_code_municipality != json_agence_code_municipality:
        final_agence_municipality=""
        final_agence_region=""
        
        while i < int(data.get('children')): #nombre de municipality dans le region  
            json_agence_code_municipality=self.correct(data.get('locations')[i].get('code'))
            final_agence_municipality=""
            final_agence_region=""
            if agence_code_municipality == json_agence_code_municipality:

                final_agence_region=self.correct(data.get('label'))
                final_agence_municipality=self.correct(data.get('locations')[i].get('label'))
                print(agence_code_municipality,"  ",agence_code_region)
                print(final_agence_municipality," ", final_agence_region)
                break
            else:
                i=i+1
        if final_agence_municipality != "" or final_agence_region != "" :
            myItem['VILLE']=final_agence_municipality
            myItem['PROVINCE']=final_agence_region
        else:
            myItem['VILLE']=""
            myItem['PROVINCE']=""

        request = scrapy.Request(full_url_telephone, callback = self.detail_page)
        request.meta["myItem"] = myItem

        yield request

#**********************numero telephone *************
    def detail_page(self, response):
        body_json=response.body.decode('utf8')
        data = json.loads(body_json)
        myItem = response.meta['myItem']
        try:
            myItem['TELEPHONE'] = self.correct(data.get('phones',[])[0].get('label'))
        except:
            pass
        yield myItem    
