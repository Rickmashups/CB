﻿# -*- coding: utf-8 -*-
import urllib, urlparse, sys, xbmcplugin ,xbmcgui, xbmcaddon, xbmc, os, json, hashlib, re, urllib2, htmlentitydefs

Versao = "18.08.23"

AddonID = 'plugin.video.CubePlay'
Addon = xbmcaddon.Addon(AddonID)
AddonName = Addon.getAddonInfo("name")
icon = Addon.getAddonInfo('icon')

addonDir = Addon.getAddonInfo('path').decode("utf-8")
iconsDir = os.path.join(addonDir, "resources", "images")

libDir = os.path.join(addonDir, 'resources', 'lib')
sys.path.insert(0, libDir)
import common

addon_data_dir = xbmc.translatePath(Addon.getAddonInfo("profile")).decode("utf-8")
cacheDir = os.path.join(addon_data_dir, "cache")
if not os.path.exists(cacheDir):
	os.makedirs(cacheDir)

cadulto = Addon.getSetting("cadulto")
cPage = Addon.getSetting("cPage") # dublado redecanais
cPageleg = Addon.getSetting("cPageleg")
cPagenac = Addon.getSetting("cPagenac")
cPagelan = Addon.getSetting("cPagelan")
cPageser = Addon.getSetting("cPageser")
cPageani = Addon.getSetting("cPageani")
cPagedes = Addon.getSetting("cPagedes")
cPagefo1 = Addon.getSetting("cPagefo1")
cPageMMf = Addon.getSetting("cPageMMf")
cPageGOf = Addon.getSetting("cPageGOf")

cEPG = Addon.getSetting("cEPG")
cOrdFO = "date" if Addon.getSetting("cOrdFO")=="0" else "title"
cOrdRCF = "date" if Addon.getSetting("cOrdRCF")=="0" else "title"
cOrdRCS = "date" if Addon.getSetting("cOrdRCS")=="0" else "title"
cOrdNCF = Addon.getSetting("cOrdNCF")
cOrdNCS = Addon.getSetting("cOrdNCS")

Cat = Addon.getSetting("Cat")
Catfo = Addon.getSetting("Catfo")
CatMM = Addon.getSetting("CatMM")
CatGO = Addon.getSetting("CatGO")

Clista=[ "todos",                     "acao", "animacao", "aventura", "comedia", "drama", "fantasia", "ficcao-cientifica", "romance", "suspense", "terror"]
Clista2=["Sem filtro (Mostrar Todos)","Acao", "Animacao", "Aventura", "Comedia", "Drama", "Fantasia", "Ficcao-Cientifica", "Romance", "Suspense", "Terror"]
Clista3=["Sem filtro (Mostrar Todos)","Ação", "Animação", "Aventura", "Comédia", "Drama", "Fantasia", "Ficção-Científica", "Romance", "Suspense", "Terror"]
Clistafo0=[ "0",                        "48",         "3",    "7",        "8",        "5",       "4",      "14",                "16",      "15",       "11"]
Clistafo1=["Sem filtro (Mostrar Todos)","Lançamentos","Ação", "Animação", "Aventura", "Comédia", "Drama",  "Ficção-Científica", "Romance", "Suspense", "Terror"]
ClistaMM0=["lancamentos","acao","animacao","aventura","comedia","drama","fantasia","ficcao-cientifica","guerra","policial","romance","suspense","terror"]
ClistaMM1=["Lançamentos","Ação","Animação","Aventura","Comédia","Drama","Fantasia","F. Científica",    "Guerra","Policial","Romance","Suspense","Terror"]
ClistaGO0=["all",                       "lancamentos","acao","animacao","aventura","comedia","drama","ficcao-cientifica","guerra","policial","romance","suspense","terror"]
ClistaGO1=["Sem filtro (Mostrar Todos)","Lançamentos","Ação","Animação","Aventura","Comédia","Drama","Ficção-Científica","Guerra","Policial","Romance","Suspense","Terror"]

def setViewS():
	xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
def setViewM():
	xbmcplugin.setContent(int(sys.argv[1]), 'movies')
	
favfilmesFile = os.path.join(addon_data_dir, 'favoritesf.txt')
favseriesFile = os.path.join(addon_data_dir, 'favoritess.txt')
historicFile = os.path.join(addon_data_dir, 'historic.txt')

	
makeGroups = "true"
URLP="http://cubeplay.000webhostapp.com/"
#URLP="http://localhost:8080/"
URLNC=URLP+"cloud/v2/nc/"
URLFO=URLP+"fo/"
	
def getLocaleString(id):
	return Addon.getLocalizedString(id).encode('utf-8')

def Categories(): #70
	#AddDir("[B]!{0}: {1}[/B] - {2} ".format(getLocaleString(30036), getLocaleString(30037) if makeGroups else getLocaleString(30038) , getLocaleString(30039)), "setting" ,50 ,os.path.join(iconsDir, "setting.png"), isFolder=False)
	AddDir("[COLOR white][B][Canais de TV][/B][/COLOR]" , "", 100, "http://oi68.tinypic.com/116jn69.jpg", "http://oi68.tinypic.com/116jn69.jpg")
	AddDir("[B][COLOR white][Filmes][/COLOR][/B]", "" , -2,"https://walter.trakt.tv/images/movies/000/191/797/fanarts/thumb/6049212229.jpg", "https://walter.trakt.tv/images/movies/000/191/797/fanarts/thumb/6049212229.jpg", isFolder=True)
	AddDir("[COLOR white][B][Séries/Animes/Desenhos][/B][/COLOR]" , "", -3, "https://walter.trakt.tv/images/shows/000/098/898/fanarts/thumb/bca6f8bc3c.jpg", "https://walter.trakt.tv/images/shows/000/098/898/fanarts/thumb/bca6f8bc3c.jpg")
	AddDir("[COLOR gold][B][Filmes Favoritos Cube Play][/B][/COLOR]", "" ,301 , "http://icons.iconarchive.com/icons/royalflushxx/systematrix/256/Favorites-icon.png", "http://icons.iconarchive.com/icons/royalflushxx/systematrix/256/Favorites-icon.png")
	AddDir("[COLOR gold][B][Séries Favoritas Cube Play][/B][/COLOR]", "" ,302 , "http://icons.iconarchive.com/icons/royalflushxx/systematrix/256/Favorites-icon.png", "http://icons.iconarchive.com/icons/royalflushxx/systematrix/256/Favorites-icon.png")
	AddDir("[COLOR green][B][Histórico Filmes][/B][/COLOR]", "" ,305 , "https://cdn2.iconfinder.com/data/icons/business-office-icons/256/To-do_List-512.png", "https://cdn2.iconfinder.com/data/icons/business-office-icons/256/To-do_List-512.png")
	AddDir("[COLOR pink][B][Busca][/B][/COLOR]" , "", 160, "https://azure.microsoft.com/svghandler/search/?width=400&height=315", "https://azure.microsoft.com/svghandler/search/?width=400&height=315")
	AddDir("[B][Sobre o Addon][/B]", "" ,0 ,"http://www.iconsplace.com/icons/preview/orange/about-256.png", "http://www.iconsplace.com/icons/preview/orange/about-256.png", isFolder=False, info="Addon modificado do PlaylistLoader 1.2.0 por Avigdor\r https://github.com/avigdork/xbmc-avigdork.\r\nNão somos responsáveis por colocar o conteudo online, apenas indexamos os vídeos disponíveis na internet.\r\nVersão atual: "+Versao)
	AddDir("[B][COLOR orange][Checar Atualizações][/COLOR][/B]", "" , 200,"https://accelerator-origin.kkomando.com/wp-content/uploads/2015/04/update2-970x546.jpg", "https://accelerator-origin.kkomando.com/wp-content/uploads/2015/04/update2-970x546.jpg", isFolder=False, info="Checar se há atualizações\n\nAs atualizações normalmente são automáticas\nUse esse recurso caso não esteja recebendo automaticamente\r\nVersão atual: "+Versao)
# --------------  Menu
def MCanais(): #-1
	AddDir("[B][COLOR cyan][Filmes Lançamentos MMFilmes.tv][/COLOR][/B]", "config" , 100,"https://walter.trakt.tv/images/movies/000/191/797/fanarts/thumb/6049212229.jpg", "https://walter.trakt.tv/images/movies/000/191/797/fanarts/thumb/6049212229.jpg", isFolder=True)
	link = common.OpenURL("https://pastebin.com/raw/31SLZ8D8")
	match = re.compile('(.+);(.+)').findall(link)
	for name2,url2 in match:
		AddDir("[COLOR while][B]["+name2+"][/COLOR][/B]" , url2, 102, "http://oi68.tinypic.com/116jn69.jpg", "http://oi68.tinypic.com/116jn69.jpg")
	setViewM()
def MFilmes(): #-2
	#AddDir("[COLOR white][B][Filmes Dublado/Legendado][/B][/COLOR]" , cPage, 220, "https://walter.trakt.tv/images/movies/000/222/254/fanarts/thumb/401d5f083e.jpg", "https://walter.trakt.tv/images/movies/000/222/254/fanarts/thumb/401d5f083e.jpg", background="cPage")
	AddDir("[B][COLOR cyan][Filmes Lançamentos MMFilmes.tv][/COLOR][/B]", "config" , 184,"https://walter.trakt.tv/images/movies/000/191/797/fanarts/thumb/6049212229.jpg", "https://walter.trakt.tv/images/movies/000/191/797/fanarts/thumb/6049212229.jpg", isFolder=True)
	AddDir("[B][COLOR cyan][Filmes MMFilmes.tv][/COLOR][/B]", "config" , 180,"https://walter.trakt.tv/images/movies/000/191/797/fanarts/thumb/6049212229.jpg", "https://walter.trakt.tv/images/movies/000/191/797/fanarts/thumb/6049212229.jpg", isFolder=True)
	#AddDir("[COLOR maroon][B][Filmes GoFilmes.me][/B][/COLOR]" , "", 210, "https://walter.trakt.tv/images/movies/000/219/436/fanarts/thumb/0ff039faa5.jpg", "https://walter.trakt.tv/images/movies/000/219/436/fanarts/thumb/0ff039faa5.jpg")
	AddDir("[COLOR yellow][B][Filmes NetCine.us][/B][/COLOR]" , "", 71, "https://walter.trakt.tv/images/movies/000/181/312/fanarts/thumb/e30b344522.jpg", "https://walter.trakt.tv/images/movies/000/181/312/fanarts/thumb/e30b344522.jpg")
	AddDir("[COLOR blue][B][Filmes Lançamentos RedeCanais.com][/B][/COLOR]" , cPage, 221, "https://walter.trakt.tv/images/movies/000/222/216/fanarts/thumb/6f9bb1a733.jpg", "https://walter.trakt.tv/images/movies/000/222/216/fanarts/thumb/6f9bb1a733.jpg", background="cPage")
	AddDir("[COLOR blue][B][Filmes Dublado RedeCanais.com][/B][/COLOR]" , cPage, 90, "https://walter.trakt.tv/images/movies/000/222/254/fanarts/thumb/401d5f083e.jpg", "https://walter.trakt.tv/images/movies/000/222/254/fanarts/thumb/401d5f083e.jpg", background="cPage")
	AddDir("[COLOR blue][B][Filmes Legendado RedeCanais.com][/B][/COLOR]" , cPageleg, 91, "https://walter.trakt.tv/images/movies/000/181/313/fanarts/thumb/cc9226edfe.jpg", "https://walter.trakt.tv/images/movies/000/181/313/fanarts/thumb/cc9226edfe.jpg", background="cPageleg")
	AddDir("[COLOR blue][B][Filmes Nacional RedeCanais.com][/B][/COLOR]" , cPagenac, 92, "http://cdn.cinepop.com.br/2016/11/minhamaeeumapeca2_2-750x380.jpg", "http://cdn.cinepop.com.br/2016/11/minhamaeeumapeca2_2-750x380.jpg", background="cPagenac")
	AddDir("[COLOR purple][B][Filmes FilmesOnline.online][/B][/COLOR]" , "", 170, "https://walter.trakt.tv/images/movies/000/167/163/fanarts/thumb/23ecb5f950.jpg.webp", "https://walter.trakt.tv/images/movies/000/167/163/fanarts/thumb/23ecb5f950.jpg.webp")
	setViewM()
def MSeries(): #-3
	AddDir("[COLOR yellow][B][Séries NetCine.us][/B][/COLOR]" , "", 60, "https://walter.trakt.tv/images/shows/000/098/898/fanarts/thumb/bca6f8bc3c.jpg", "https://walter.trakt.tv/images/shows/000/098/898/fanarts/thumb/bca6f8bc3c.jpg")
	AddDir("[COLOR blue][B][Séries RedeCanais.com][/B][/COLOR]" , cPageser, 130, "https://walter.trakt.tv/images/shows/000/001/393/fanarts/thumb/fc68b3b649.jpg", "https://walter.trakt.tv/images/shows/000/001/393/fanarts/thumb/fc68b3b649.jpg", background="cPageser")
	AddDir("[COLOR blue][B][Animes RedeCanais.com][/B][/COLOR]" , cPageser, 140, "https://walter.trakt.tv/images/shows/000/098/580/fanarts/thumb/d48b65c8a1.jpg", "https://walter.trakt.tv/images/shows/000/098/580/fanarts/thumb/d48b65c8a1.jpg", background="cPageser")
	AddDir("[COLOR blue][B][Desenhos RedeCanais.com][/B][/COLOR]" , cPageani, 150, "https://walter.trakt.tv/images/shows/000/069/829/fanarts/thumb/f0d18d4e1d.jpg", "https://walter.trakt.tv/images/shows/000/069/829/fanarts/thumb/f0d18d4e1d.jpg", background="cPageser")
	AddDir("[B][COLOR cyan][Séries MMFilmes.tv][/COLOR][/B]", "config" , 190,"https://walter.trakt.tv/images/shows/000/037/522/fanarts/thumb/6ecdb75c1c.jpg", "https://walter.trakt.tv/images/shows/000/037/522/fanarts/thumb/6ecdb75c1c.jpg", isFolder=True)
	setViewM()
# --------------  Fim menu
# --------------  Inicio Filme CB
def Filmes96(): #220
	link = common.OpenURL("https://pastebin.com/raw/ZkfFMB20")
	m = link.split("\n")
	for x in m:
		try:
			meta = eval(x)
			AddDir(meta['title'] +" [COLOR yellow]("+str(meta['year'])+")[/COLOR] "+" [COLOR blue]["+str(meta['rating'])+"][/COLOR]" , meta['mp4'] +"?play", 229, isFolder=False, IsPlayable=True, metah=meta)
		except:
			pass
	setViewM()
def FilmesRC(): #221
	link = common.OpenURL("https://pastebin.com/raw/taJHVbXj")
	m = link.split("\n")
	link2 = common.OpenURL("https://pastebin.com/raw/FwSnnr65")
	i=1
	for x in m:
		try:
			meta = eval(x)
			file = meta['mp4'].split("$")
			reg = "(.+)\$"+file[1]
			m = re.compile(reg, re.IGNORECASE).findall(link2)
			url2 = m[0]
			AddDir(meta['title'] +" [COLOR yellow]("+str(meta['year'])+")[/COLOR] "+" [COLOR blue]["+str(meta['rating'])+"][/COLOR]" , url2 + file[0] +"?play|Referer=http://redecanais.cz/", 229, isFolder=False, IsPlayable=True, metah=meta)
		except:
			pass
	setViewM()
def PlayFilmes96(): #229
	PlayUrl(name, url, iconimage, info, "", metah)
# --------------  Fim Filme CB
# --------------  NETCINE
def CategoryOrdem(x):
	x2 = Addon.getSetting(eval("x"))
	name2 = "Data" if x2=="0" else "Título"
	AddDir("[COLOR green][B][Organizado por:][/B] "+name2 +" (Clique para alterar)[/COLOR]" , x, 81, "https://lh5.ggpht.com/gv992ET6R_InCoMXXwIbdRLJczqOHFfLxIeY-bN2nFq0r8MDe-y-cF2aWq6Qy9P_K-4=w300", "https://lh5.ggpht.com/gv992ET6R_InCoMXXwIbdRLJczqOHFfLxIeY-bN2nFq0r8MDe-y-cF2aWq6Qy9P_K-4=w300", isFolder=False)
def CategoryOrdem2(url):
	x2 = Addon.getSetting(url)
	x = "0" if x2=="1" else "1"
	#xbmcgui.Dialog().ok("Escolha a resolução:", x + x2 + url)
	Addon.setSetting(url, x )
	xbmc.executebuiltin("XBMC.Container.Refresh()")
def Series(): #60
	try:
		CategoryOrdem("cOrdNCS")
		link = common.OpenURL("http://netcine.us/tvshows/page/1/").replace('\n','').replace('\r','')
		l2 = re.compile("box_movies(.+)").findall(link)
		link = common.OpenURL("http://netcine.us/tvshows/page/2/").replace('\n','').replace('\r','')
		l3 = re.compile("box_movies(.+)").findall(link)
		lista = re.compile("img src\=\"([^\"]+).+?alt\=\"([^\"]+).+?f\=\"([^\"]+)").findall(l2[0]+l3[0])
		if cOrdNCS=="1":
			lista = sorted(lista, key=lambda lista: lista[1])
		for img2,name2,url2 in lista:
			if name2!="Close":
				name2 = name2.replace("&#8211;","-").replace("&#038;","&").replace("&#8217;","\'")
				img2 = re.sub('-120x170.(jpg|png)', r'.\1', img2 )
				AddDir(name2 ,url2, 61, img2, img2, isFolder=True)
	except:
		AddDir("Server NETCINE offline, tente novamente em alguns minutos" , "", 0, isFolder=False)
def ListSNC(x): #61
	try:
		link = common.OpenURL(url).replace('\n','').replace('\r','').replace('<div class="soci">',"class='has-sub'").replace('\t',"")
		m = re.compile("(.emporada \w+)(.+?class\=\'has-sub\')").findall(link)
		info2 = re.compile("<h2>Synopsis<\/h2>+.+?[div|p].{0,15}?.+?(.+?)<\/").findall(link)
		info2 = re.sub('style\=.+?\>', '', info2[0] ) if info2 else " "
		i=0
		if "None" in background:
			for season,epis in m:
				AddDir("[B]["+season+"][/B]" ,url, 61, iconimage, iconimage, isFolder=True, background=i,info=info2)
				i+=1
		else:
			m2 = re.compile("href\=\"([^\"]+).+?(\d+) - (\d+)").findall( m[int(x)][1] )
			m3 = re.compile("icon-chevron-right\W+\w\W+([^\<]+)").findall( m[int(x)][1] )
			for url2,S,E in m2:
				AddDir("S"+S+"E"+E +" - "+m3[i],url2, 62, iconimage, iconimage, isFolder=False, IsPlayable=True, info=info)
				i+=1
	except:
		AddDir("Server NETCINE offline, tente novamente em alguns minutos" , "", 0, isFolder=False)
def PlayS(): #62
	try:
		link = common.OpenURL(url).replace('\n','').replace('\r','')
		m = re.compile("\"play-.\".+?src=\"([^\"]+)").findall(link)
		listan = re.compile("\#play-...(\w*)").findall(link)
		i=0
		listaf=[]
		listal=[]
		for url2 in m:
			link3 = common.OpenURL(url2)
			m3 = re.compile("(campanha\d?).php?([^\"]+)").findall(link3)
			if m3:
				for url3 in m3:
					if url3[0] == "campanha":
						cp = "desktop22"
					elif url3[0] == "campanha2":
						cp = "desktop20"
					else:
						cp = "desktopnovo"
					link4 = common.OpenURL("http://p.netcine.us/players/"+cp+".php"+url3[1])
					link4 = re.sub('window.location.+', '', link4)
					m4= re.compile("http.+?mp4[^\"]+").findall(link4) 
					m4 = list(reversed(m4))
					for url4 in m4:
						listal.append(url4)
						dubleg="[COLOR green]HD[/COLOR][/B]" if "ALTO" in url4 else "[COLOR red]SD[/COLOR][/B]"
						listaf.append("[B][COLOR blue]"+listan[i] +"[/COLOR] "+dubleg)
			else:
					m4= re.compile("http\:\/\/.+[ALTO|BAIXO].mp4[^\"]+").findall(link3)
					m4 = list(reversed(m4))
					ST(link3)
					for url4 in m4:
						listal.append(url4)
						dubleg="[COLOR green]HD[/COLOR][/B]" if "ALTO" in url4 else "[COLOR red]SD[/COLOR][/B]"
						listaf.append("[B][COLOR blue]"+listan[i] +"[/COLOR] "+dubleg)
			i+=1
		d = xbmcgui.Dialog().select("Escolha a resolução:", listaf)
		if d!= -1:
			PlayUrl(name, listal[d], iconimage, info)
	except:
		xbmcgui.Dialog().ok('Cube Play', 'Erro, tente novamente em alguns minutos')
# --------------------------------------
def MoviesNC(): #71
	AddDir("[COLOR yellow][B][Genero dos Filmes]:[/B] " + Clista3[int(Cat)] +"[/COLOR]", "url" ,80 ,"https://lh5.ggpht.com/gv992ET6R_InCoMXXwIbdRLJczqOHFfLxIeY-bN2nFq0r8MDe-y-cF2aWq6Qy9P_K-4=w300", "https://lh5.ggpht.com/gv992ET6R_InCoMXXwIbdRLJczqOHFfLxIeY-bN2nFq0r8MDe-y-cF2aWq6Qy9P_K-4=w300", isFolder=False)
	CategoryOrdem("cOrdNCF")
	try:
		if Cat=="0":
			link = common.OpenURL("http://netcine.us/page/1/?mt").replace('\n','').replace('\r','')
			l1 = re.compile("box_movies(.+)").findall(link)
			link = common.OpenURL("http://netcine.us/page/2/?mt").replace('\n','').replace('\r','')
			l2 = re.compile("box_movies(.+)").findall(link)
			link = common.OpenURL("http://netcine.us/page/3/?mt").replace('\n','').replace('\r','')
			l3 = re.compile("box_movies(.+)").findall(link)
			lista = re.compile("img src\=\"([^\"]+).+?alt\=\"([^\"]+).+?f\=\"([^\"]+)").findall(l1[0]+l2[0]+l3[0])
		else:
			link = common.OpenURL("http://netcine.us/category/"+Clista[int(Cat)]).replace('\n','').replace('\r','')
			l2 = re.compile("box_movies(.+)").findall(link)
			lista = re.compile("img src\=\"([^\"]+).+?alt\=\"([^\"]+).+?f\=\"([^\"]+)").findall(l2[0])
		if cOrdNCF=="1":
			lista = sorted(lista, key=lambda lista: lista[1])
		for img2,name2,url2 in lista:
			if name2!="Close":
				name2 = name2.replace("&#8211;","-").replace("&#038;","&").replace("&#8217;","\'")
				img2 = re.sub('-120x170.(jpg|png)', r'.\1', img2 )
				AddDir(name2 ,url2, 78, img2, img2, isFolder=True)
	except urllib2.URLError, e:
		AddDir("Server NETCINE offline, tente novamente em alguns minutos" , "", 0, isFolder=False)
def ListMoviesNC(): #78
	try:
		link = common.OpenURL(url).replace('\n','').replace('\r','')
		m = re.compile("\"play-.\".+?src=\"([^\"]+)").findall(link)
		m2 = re.compile("\#play-...(\w*)").findall(link)
		info2 = re.compile("<h2>Synopsis<\/h2>+.+?[div|p].{0,15}?.+?(.+?)<\/").findall(link)
		info2 = re.sub('style\=.+?\>', '', info2[0] ) if info2 else ""
		i=0
		for name2 in m2:
			AddDir(name +" [COLOR blue]("+ name2 +")[/COLOR]", m[i], 79, iconimage, iconimage, isFolder=False, IsPlayable=True, info=info2, background=url)
			i+=1
	except urllib2.URLError, e:
		AddDir("Server error, tente novamente em alguns minutos" , "", 0, isFolder=False)
def PlayMNC(): #79
	try:
		link = common.OpenURL(url)
		m = re.compile("http.+netcine[^\"]+").findall(link)
		link1 = common.OpenURL(m[0])
		m1 = re.compile("http.+netcine[^\"]+").findall(link1)
		link2 = common.OpenURL(m1[1])
		link2 = re.sub('window.location.+', '', link2)
		m2 = re.compile("http.+?mp4[^\"]+").findall(link2)
		if m2:
			m2 = list(reversed(m2))
			lista =[]
			for url2 in m2:
				lista.append( "[B][COLOR green]HD[/COLOR][/B]" if "ALTO" in url2 else "[B][COLOR red]SD[/COLOR][/B]")
			d = xbmcgui.Dialog().select("Escolha a resolução:", lista)
			if d!= -1:
				global background
				background=background+";;;"+name+";;;NC"
				PlayUrl(name, m2[d], iconimage, info)
	except urllib2.URLError, e:
		xbmcgui.Dialog().ok('Cube Play', 'Erro, tente novamente em alguns minutos')
def Generos(): #80
	d = xbmcgui.Dialog().select("Escolha o Genero", Clista3)
	if d != -1:
		global Cat
		Addon.setSetting("Cat", str(d) )
		Cat = d
		Addon.setSetting("cPage", "0" )
		Addon.setSetting("cPageleg", "0" )
		xbmc.executebuiltin("XBMC.Container.Refresh()")
# --------------  FIM NETCINE
# --------------  REDECANAIS FILMES
def MoviesRCD(): #90 Filme dublado
	AddDir("[COLOR yellow][B][Genero dos Filmes]:[/B] " + Clista3[int(Cat)] +"[/COLOR]", "url" ,80 ,"https://lh5.ggpht.com/gv992ET6R_InCoMXXwIbdRLJczqOHFfLxIeY-bN2nFq0r8MDe-y-cF2aWq6Qy9P_K-4=w300", "https://lh5.ggpht.com/gv992ET6R_InCoMXXwIbdRLJczqOHFfLxIeY-bN2nFq0r8MDe-y-cF2aWq6Qy9P_K-4=w300", isFolder=False)
	CategoryOrdem("cOrdRCF")
	try:
		p= 1
		if int(cPage) > 0:
			AddDir("[COLOR blue][B]<< Pagina Anterior ["+ str( int(cPage) ) +"[/B]][/COLOR]", cPage , 120 ,"http://icons.iconarchive.com/icons/iconsmind/outline/256/Previous-icon.png", isFolder=False, background="cPage")
		l= int(cPage)*5
		for x in range(0, 5):
			l +=1
			link = common.OpenURL("http://www.redecanais.cz/browse-filmes-dublado-videos-"+str(l)+"-"+cOrdRCF+".html")
			if Clista2[int(Cat)] != "Sem filtro (Mostrar Todos)":
				link = common.OpenURL("http://www.redecanais.cz/browse-"+Clista2[int(Cat)]+"-Filmes-videos-"+str(l)+"-"+cOrdRCF+".html")
			match = re.compile('href=\"([^\"]+).{70,90}src=\"([^\"]+)\".alt=\"([^\"]+)').findall(link)
			if match:
				for url2,img2,name2 in match:
					url2 = re.sub('^\.', "http://www.redecanais.cz/", url2 )
					AddDir(name2 ,url2, 95, img2, img2, info="")
					p += 1
			else:
				break
		if p >= 60:
			AddDir("[COLOR blue][B]Proxima Pagina >> ["+ str( int(cPage) + 2) +"[/B]][/COLOR]", cPage , 110 ,"http://icons.iconarchive.com/icons/iconsmind/outline/256/Next-2-2-icon.png", isFolder=False, background="cPage")
	except:
		AddDir("Server error, tente novamente em alguns minutos" , "", 0, "", "")
def MoviesRCL(): #91 Filme Legendado
	AddDir("[COLOR yellow][B][Genero dos Filmes]:[/B] " + Clista3[int(Cat)] +"[/COLOR]", "url" ,80 ,"https://lh5.ggpht.com/gv992ET6R_InCoMXXwIbdRLJczqOHFfLxIeY-bN2nFq0r8MDe-y-cF2aWq6Qy9P_K-4=w300", "https://lh5.ggpht.com/gv992ET6R_InCoMXXwIbdRLJczqOHFfLxIeY-bN2nFq0r8MDe-y-cF2aWq6Qy9P_K-4=w300", isFolder=False)
	CategoryOrdem("cOrdRCF")
	try:
		p= 1
		if int(cPageleg) > 0:
			AddDir("[COLOR blue][B]<< Pagina Anterior ["+ str( int(cPageleg) ) +"[/B]][/COLOR]", cPageleg , 120 ,"http://icons.iconarchive.com/icons/iconsmind/outline/256/Previous-icon.png", isFolder=False, background="cPageleg")
		l= int(cPageleg)*5
		for x in range(0, 5):
			l +=1
			link = common.OpenURL("http://www.redecanais.cz/browse-filmes-legendado-videos-"+str(l)+"-"+cOrdRCF+".html")
			if Clista2[int(Cat)] != "Sem filtro (Mostrar Todos)":
				link = common.OpenURL("http://www.redecanais.cz/browse-"+Clista2[int(Cat)]+"-Filmes-Legendado-videos-"+str(l)+"-"+cOrdRCF+".html")
			match = re.compile('href=\"([^\"]+).{70,90}src=\"([^\"]+)\".alt=\"([^\"]+)').findall(link)
			if match:
				for url2,img2,name2 in match:
					url2 = re.sub('^\.', "http://www.redecanais.cz/", url2 )
					AddDir(name2 ,url2, 95, img2, img2, info="")
					p += 1
			else:
				break
		if p >= 60:
			AddDir("[COLOR blue][B]Proxima Pagina >> ["+ str( int(cPageleg) + 2) +"[/B]][/COLOR]", cPageleg , 110 ,"http://icons.iconarchive.com/icons/iconsmind/outline/256/Next-2-2-icon.png", isFolder=False, background="cPageleg")
	except:
		AddDir("Server error, tente novamente em alguns minutos" , "", 0, "", "")
def MoviesRCN(): #92 Filmes Nacional
	CategoryOrdem("cOrdRCF")
	try:
		p= 1
		if int(cPagenac) > 0:
			AddDir("[COLOR blue][B]<< Pagina Anterior ["+ str( int(cPagenac) ) +"[/B]][/COLOR]", cPagenac , 120 ,"http://icons.iconarchive.com/icons/iconsmind/outline/256/Previous-icon.png", isFolder=False, background="cPagenac")
		l= int(cPagenac)*5
		for x in range(0, 5):
			l +=1
			link = common.OpenURL("http://www.redecanais.cz/browse-filmes-nacional-videos-"+str(l)+"-"+cOrdRCF+".html")
			match = re.compile('href=\"([^\"]+).{70,90}src=\"([^\"]+)\".alt=\"([^\"]+)').findall(link)
			if match:
				for url2,img2,name2 in match:
					url2 = re.sub('^\.', "http://www.redecanais.cz/", url2 )
					AddDir(name2 ,url2, 95, img2, img2, info="")
					p += 1
			else:
				break
		if p >= 60:
			AddDir("[COLOR blue][B]Proxima Pagina >> ["+ str( int(cPagenac) + 2) +"[/B]][/COLOR]", cPagenac , 110 ,"http://icons.iconarchive.com/icons/iconsmind/outline/256/Next-2-2-icon.png", isFolder=False, background="cPagenac")
	except:
		AddDir("Server error, tente novamente em alguns minutos" , "", 0, "", "", 0)
def MoviesRCR(): # Lancamentos
	#CategoryOrdem("cOrdRCF")
	try:
		p= 1
		if int(cPagelan) > 0:
			AddDir("[COLOR blue][B]<< Pagina Anterior ["+ str( int(cPagelan) ) +"[/B]][/COLOR]", cPagelan , 120 ,"http://icons.iconarchive.com/icons/iconsmind/outline/256/Previous-icon.png", isFolder=False, background="cPagelan")
		l= int(cPagelan)*5
		for x in range(0, 5):
			l +=1
			link = common.OpenURL("https://www.redecanais.cz/browse-filmes-lancamentos-videos-"+str(l)+"-date.html")
			match = re.compile('href=\"([^\"]+).{70,90}src=\"([^\"]+)\".alt=\"([^\"]+)').findall(link)
			if match:
				for url2,img2,name2 in match:
					url2 = re.sub('^\.', "http://www.redecanais.cz/", url2 )
					AddDir(name2 ,url2, 95, img2, img2, info="")
					p += 1
			else:
				break
		if p >= 60:
			AddDir("[COLOR blue][B]Proxima Pagina >> ["+ str( int(cPagelan) + 2) +"[/B]][/COLOR]", cPagelan , 110 ,"http://icons.iconarchive.com/icons/iconsmind/outline/256/Next-2-2-icon.png", isFolder=False, background="cPagelan")
	except:
		AddDir("Server error, tente novamente em alguns minutos" , "", 0, "", "", 0)
def PlayMRC(): #95 Play filmes
	try:
		link = common.OpenURL(url.replace("https","http"))
		desc = re.compile('<p itemprop=\"description\"><p>(.+)<\/p><\/p>').findall(link)
		if desc:
			desc = re.sub('&([^;]+);', lambda m: unichr(htmlentitydefs.name2codepoint[m.group(1)]), desc[0]).encode('utf-8')
		player = re.compile('<iframe name=\"Player\".{1,8}src=\"([^\"]+)\"').findall(link)
		if player:
			mp4 = common.OpenURL(player[0])
			mmp4 = re.compile('http.{5,95}mp4').findall(mp4)
			AddDir("[B][COLOR yellow]"+ name +" [/COLOR][/B]"  , mmp4[0] + "?play|Referer="+player[0], 3, iconimage, iconimage, index=0, isFolder=False, IsPlayable=True, info=desc, background=url+";;;"+name+";;;RC")
		else:
			AddDir("[B]Ocorreu um erro[/B]"  , "", 0, iconimage, iconimage, index=0, isFolder=False, IsPlayable=False, info="Erro")
	except:
		AddDir("Server error, tente novamente em alguns minutos" , "", 0, "", "")
# ----------------- FIM REDECANAIS
# --------------  REDECANAIS SERIES,ANIMES,DESENHOS
def PlaySRC(): #133 Play series
	try:
		url2 = re.sub('redecanais\.[^\/]+', "redecanais.cz", url.replace("https","http") )
		link = common.OpenURL(url2)
		desc = re.compile('<p itemprop=\"description\"><p>(.+)<\/p><\/p>').findall(link)
		if desc:
			desc = re.sub('&([^;]+);', lambda m: unichr(htmlentitydefs.name2codepoint[m.group(1)]), desc[0]).encode('utf-8')
		player = re.compile('<iframe name=\"Player\".+src=\"([^\"]+)\"').findall(link)
		if player:
			mp4 = common.OpenURL(player[0])
			mmp4 = re.compile('http.{5,95}mp4').findall(mp4)
			PlayUrl(name, mmp4[0] + "?play|Referer="+player[0], iconimage, name)
		else:
			xbmcgui.Dialog().ok('Cube Play', 'Erro, tente novamente em alguns minutos')
	except:
		xbmcgui.Dialog().ok('Cube Play', 'Erro, tente novamente em alguns minutos')
def TemporadasRC(x): #135 Episodios
	url2 = re.sub('redecanais\.[^\/]+', "redecanais.cz", url.replace("https","http") )
	link = common.OpenURL(url2).replace('\n','').replace('\r','').replace('</html>','<span style="font').replace("https","http")
	temps = re.compile('(<span style="font-size: x-large;">(.+?)<\/span>)').findall(link)
	i= 0
	if background=="None":
		for b,tempname in temps:
			tempname = re.sub('<[\/]{0,1}strong>', "", tempname)
			try:
				tempname = re.sub('&([^;]+);', lambda m: unichr(htmlentitydefs.name2codepoint[m.group(1)]), tempname).encode('utf-8')
			except:
				tempname = tempname
			if not "ilme" in tempname:
				AddDir("[B]["+tempname+"][/B]" , url, 135, iconimage, iconimage, info="", isFolder=True, background=i)
			i+=1
		AddDir("[B][Todos Episódios][/B]" ,url, 139, iconimage, iconimage, info="")
	else:
		temps2 = re.compile('size: x-large;\">.+?<span style\=\"font').findall(link)
		epi = re.compile('<strong>(E.+?)<\/strong>(.+?)(<br|<\/p)').findall(temps2[int(x)])
		for name2,url2,brp in epi:
			name3 = re.compile('\d+').findall(name2)
			if name3:
				name3=name3[0]
			else:
				name3=name2
			urlm = re.compile('href\=\"(.+?)\"').findall(url2)
			url2 = re.sub('(\w)-(\w)', r'\1 \2', url2)
			try:
				namem = re.sub('&([^;]+);', lambda m: unichr(htmlentitydefs.name2codepoint[m.group(1)]), re.compile('([^\-]+)').findall(url2)[0] ).encode('utf-8')
			except:
				namem = re.compile('([^\-]+)').findall(url2)[0]
			namem = re.sub('<[\/]{0,1}strong>', "", namem)
			if "<" in namem:
				namem = ""
			if urlm:
				urlm[0] = "http://www.redecanais.cz/" + urlm[0] if "http" not in urlm[0] else urlm[0]
			if len(urlm) > 1:
				urlm[1] = "http://www.redecanais.cz/" + urlm[1] if "http" not in urlm[1] else urlm[1]
				AddDir("[COLOR yellow][Dub][/COLOR] "+ name3 +" "+namem ,urlm[0], 133, iconimage, iconimage, info="", isFolder=False, IsPlayable=True)
				AddDir("[COLOR blue][Leg][/COLOR] "+ name3 +" "+namem ,urlm[1], 133, iconimage, iconimage, info="", isFolder=False, IsPlayable=True)
			elif urlm:
				AddDir(name3 +" "+namem ,urlm[0], 133, iconimage, iconimage, info="", isFolder=False, IsPlayable=True)
def SeriesRC(urlrc,pagina2): #130 Lista as Series RC
	try:
		CategoryOrdem("cOrdRCS")
		pagina=eval(pagina2)
		p= 1
		if int(pagina) > 0:
			AddDir("[COLOR blue][B]<< Pagina Anterior ["+ str( int(pagina) ) +"[/B]][/COLOR]", pagina , 120 ,"http://icons.iconarchive.com/icons/iconsmind/outline/256/Previous-icon.png", isFolder=False, background=pagina2)
		l= int(pagina)*5
		for x in range(0, 5):
			l +=1
			link = common.OpenURL("http://www.redecanais.cz/browse-"+urlrc+"-videos-"+str(l)+"-"+cOrdRCS+".html")
			match = re.compile('href=\"([^\"]+).{70,90}src=\"([^\"]+)\".alt=\"([^\"]+)').findall(link)
			if match:
				for url2,img2,name2 in match:
					url2 = re.sub('^\.', "http://www.redecanais.cz/", url2 )
					if not "index.html" in url2:
						AddDir(name2 ,url2, 135, img2, img2, info="")
						p += 1
			else:
					break
		if p >= 60:
			AddDir("[COLOR blue][B]Proxima Pagina >> ["+ str( int(pagina) + 2) +"[/B]][/COLOR]", pagina , 110 ,"http://icons.iconarchive.com/icons/iconsmind/outline/256/Next-2-2-icon.png", isFolder=False, background=pagina2)
	except urllib2.URLError, e:
		AddDir("Server error, tente novamente em alguns minutos" , url, 0, "", "")
def AllEpisodiosRC(): #139 Mostrar todos Epi
	link = common.OpenURL(url)
	match = re.compile('<strong>(E.+?)<\/strong>(.+?)(<br|<\/p)').findall(link)
	S= 0
	if match:
		for name2,url2,brp in match:
			name3 = re.compile('\d+').findall(name2)
			if name3:
				name3=name3[0]
				if int(name3) == 1:
					S = S + 1
			else:
				name3=name2

			urlm = re.compile('href\=\"(.+?)\"').findall(url2)
			try:
				namem = re.sub('&([^;]+);', lambda m: unichr(htmlentitydefs.name2codepoint[m.group(1)]), re.compile('([^\-]+)').findall(url2)[0] ).encode('utf-8')
			except:
				namem = re.compile('([^\-]+)').findall(url2)[0]
			if "<" in namem:
				namem = ""
			if urlm:
				if "http" not in urlm[0]:
					urlm[0] = "http://www.redecanais.cz/" + urlm[0]
			if len(urlm) > 1:
				if "http" not in urlm[1]:
					urlm[1] = "http://www.redecanais.cz/" + urlm[1]
				AddDir("[COLOR yellow][Dub][/COLOR] S"+str(S)+" E"+ name3 +" "+namem ,urlm[0], 133, iconimage, iconimage, info="", isFolder=False, IsPlayable=True)
				AddDir("[COLOR blue][Leg][/COLOR] S"+str(S)+" E"+ name3 +" "+namem ,urlm[1], 133, iconimage, iconimage, info="", isFolder=False, IsPlayable=True)
			elif urlm:
				AddDir("S"+str(S)+" E"+ name3 +" "+namem ,urlm[0], 133, iconimage, iconimage, info="", isFolder=False, IsPlayable=True)
# ----------------- FIM REDECANAIS SERIES,ANIMES,DESENHOS
# ----------------- BUSCA
def Busca(): # 160
	AddDir("[COLOR pink][B][Nova Busca][/B][/COLOR]", "" , 50 ,"", isFolder=False)
	d = xbmcgui.Dialog().input("Busca (poder demorar a carregar os resultados)").replace(" ", "+")
	if not d:
		return Categories()
		sys.exit(int(sys.argv[1]))
	try:
		p= 1
		AddDir("[COLOR blue][B][RedeCanais.com][/B][/COLOR]", "" , 0 ,"", isFolder=False)
		l= 0
		for x in range(0, 6):
			l +=1
			link = common.OpenURL("http://www.redecanais.cz/search.php?keywords="+d+"&page="+str(l))
			match = re.compile('href=\"([^\"]+).{70,90}src=\"([^\"]+)\".alt=\"([^\"]+)').findall(link)
			if match:
				for url2,img2,name2 in match:
					url2 = re.sub('^\.', "http://www.redecanais.cz/", url2 )
					if re.compile('\d+p').findall(name2):
						AddDir(name2 ,url2, 95, img2, img2)
					elif "Lista" in name2:
						AddDir(name2 ,url2, 135, img2, img2)
			else:
				break
	except:
		pass
	try:
		AddDir("[COLOR yellow][B][NetCine.us][/B][/COLOR]", "" , 0 ,"", isFolder=False)
		link2 = common.OpenURL("http://netcine.us/?s="+d).replace('\n','').replace('\r','')
		lista = re.compile("img src\=\"([^\"]+).+?alt\=\"([^\"]+).+?f\=\"([^\"]+)").findall(link2)
		for img2,name2,url2 in lista:
			if name2!="Close" and name2!="NetCine":
				name2 = name2.replace("&#8211;","-").replace("&#038;","&").replace("&#8217;","\'")
				img2 = re.sub('-120x170.(jpg|png)', r'.\1', img2 )
				if "tvshows" in url2:
					AddDir(name2 ,url2, 61, img2, img2, isFolder=True)
				else:
					AddDir(name2 ,url2, 78, img2, img2, isFolder=True)
	except:
		pass
	l=0
	i=0
	try:
		AddDir("[COLOR cyan][B][MMfilmes.tv][/B][/COLOR]", "" , 0 ,"", isFolder=False)
		links = common.OpenURL("http://www.mmfilmes.tv/series/")
		ms = re.compile('href\=\"(.+www.mmfilmes.tv.+)\" rel\=\"bookmark\"').findall(links)
		for x in range(0, 3):
			l+=1
			link = common.OpenURL("http://www.mmfilmes.tv/page/"+str(l)+"/?s="+d)
			m = re.compile('id\=\"post\-\d+\".+?\=.([^\"]+)\h*(?s)(.+?)(http[^\"]+)').findall(link)
			res = re.compile('audioy..([^\<]*)').findall(link)
			jpg = re.compile('src=\"(http.+?www.mmfilmes.tv\/wp-content\/uploads[^\"]+)').findall(link)
			dubleg = re.compile('boxxer.+\s.+boxxer..([^\<]*)').findall(link)
			if m:
				for name2,b,url2 in m:
					name2 = name2.replace("&#8211;","-").replace("&#038;","&").replace("&#8217;","\'")
					if not url2 in ms:
						AddDir(name2+ " [COLOR yellow]"+res[i]+"[/COLOR] [COLOR blue]"+dubleg[i]+"[/COLOR]", url2, 181, jpg[i], jpg[i],isFolder=True,IsPlayable=False)
					else:
						AddDir(name2, url2, 191, jpg[i], jpg[i], isFolder=True,IsPlayable=False)
					i+=1
			i=0
	except:
		pass
	#l=0
	#i=0
	#try:
	#	AddDir("[COLOR maroon][B][Gofilmes.me][/B][/COLOR]", "" , 0 ,"", isFolder=False)
	#	for x in range(0, 3):
	#		l+=1
	#		link = common.OpenURL("http://gofilmes.me/search?s="+d+"&p="+str(l)).replace("</div><div","\r\n")
	#		m = re.compile('href=\"([^\"]+)\" title\=\"([^\"]+).+b\" src\=\"([^\"]+).+').findall(link)
	#		for url2,name2,img2 in m:
	#			AddDir(name2, url2, 211, img2, img2, isFolder=False, IsPlayable=True)
	#except:
	#	pass
# ----------------- FIM BUSCA
# ----------------- TV Cubeplay
def TVCB(x): #102
	try:
		#AddDir("a", "", 50, "", "", isFolder=False, IsPlayable=False, info="")
		link = common.OpenURL(x)
		link = re.sub('^.{3}', "", link )
		m = re.compile('(.+)\?(.+)').findall(link)
		i=0
		for name2,url2 in m:
			if cadulto=="8080":
				AddDir(getmd5(name2), url2, 103, " ", " ", isFolder=False, IsPlayable=True, info="")
				i+=1
			elif not "dulto" in getmd5(name2):
				AddDir(getmd5(name2), url2, 103, " ", " ", isFolder=False, IsPlayable=True, info="")
				i+=1
	except:
		AddDir("Servidor offline, tente novamente em alguns minutos" , "", 0, "", "", 0)
def PlayTVCB(): #103
	try:
		PlayUrl(name, getmd5(url), "", "", "")
	except urllib2.URLError, e:
		xbmcgui.Dialog().ok('Cube Play', "Servidor offline, tente novamente em alguns minutos")
# ----------------- Fim TV Cubeplay
# ----------------- REDECANAIS TV
def Acento(x):
	x = x.replace("\xe7","ç").replace("\xe0","à").replace("\xe1","á").replace("\xe2","â").replace("\xe3","ã").replace("\xe8","è").replace("\xe9","é").replace("\xea","ê").replace("\xed","í").replace("\xf3","ó").replace("\xf4","ô").replace("\xf5","õ").replace("\xfa","ú")
	return x
def EPG():
	epg1 = "{"
	try:
		xbmc.executebuiltin("Notification({0}, {1}, 7000, {2})".format(AddonName, "Carregando lista EPG. Aguarde um momento!", icon))
		link = common.OpenURL("http://www.epg.com.br/~mysql41/vertv.php").replace('	','')
		m = re.compile('javascript:toggleCanal\(\d+,.([^\']+)\h*(?s)(.+?)\<\!-- orig').findall(link)
		for c,f in m:
			hora = ""
			m2 = re.compile('(.+)(\(\d+.\d+\))\s').findall(f)
			if m2:
				for prog1,prog2 in m2:
					hora += prog2 +" "+ prog1 + ";;;"
					try:
						hora= Acento(hora)
					except:
						hora = hora
			hora = hora.replace("'","")
			epg1 += "'"+c+"' : '"+hora+"' , "
		return epg1+"'none':''}"
	except urllib2.URLError, e:
		return ""
		xbmc.executebuiltin("Notification({0}, {1}, 7000, {2})".format(AddonName, "Erro. tente novamente!", icon))
def TVRC(): #100
	link = urllib2.urlopen("https://pastebin.com/raw/QaYHY3Nf").read().replace('\n','').replace('\r','')
	match = re.compile('url="(.+?)".+?mg="(.+?)".+?ame="(.+?)"').findall(link)
	for url2,img2,name2 in match:
		if cadulto=="8080":
			AddDir(name2, url2, 101, img2, img2, isFolder=False, IsPlayable=True, info = "")
		elif not "dulto" in name2:
			AddDir(name2, url2, 101, img2, img2, isFolder=False, IsPlayable=True, info = "")
def PlayTVRC(): # 101
	#url2 = re.sub('redecanais\.[^\/]+', "redecanais.cz", url.replace("https","http") )
	try:
		link = common.OpenURL(url)
		player = re.compile('<iframe name=\"Player\".+src=\"([^\"]+)\"').findall(link)
		link2 = common.OpenURL(player[0])
		m2 = re.compile('action="([^\"]+)').findall(link2)
		m2[0] = re.sub('.\/', 'https://canais.ink/', m2[0])
		link3 = common.OpenURL(m2[0])
		urlp = re.compile('(http[^\"]+m3u[^\"]+)').findall(link3)
		if urlp:
			PlayUrl(name, urlp[0] + "?play|Referer="+player[0], iconimage, info)
		else:
			xbmcgui.Dialog().ok('Cube Play', "Erro, aguarde atualização")
	except:
		xbmcgui.Dialog().ok('Cube Play', 'Erro, tente novamente em alguns minutos')
# ----------------- FIM REDECANAIS TV
# ----------------- Inicio Filmes Online
def GenerosFO(): #85
	d = xbmcgui.Dialog().select("Escolha o Genero", Clistafo1)
	if d != -1:
		global Cat
		Addon.setSetting("Catfo", str(d) )
		Cat = d
		Addon.setSetting("cPagefo1", "0" )
		xbmc.executebuiltin("XBMC.Container.Refresh()")
		
def MoviesFO(urlfo,pagina2): #170
	AddDir("[COLOR yellow][B][Gênero dos Filmes]:[/B] " + Clistafo1[int(Catfo)] +"[/COLOR]", "url" ,85 ,"https://lh5.ggpht.com/gv992ET6R_InCoMXXwIbdRLJczqOHFfLxIeY-bN2nFq0r8MDe-y-cF2aWq6Qy9P_K-4=w300", "https://lh5.ggpht.com/gv992ET6R_InCoMXXwIbdRLJczqOHFfLxIeY-bN2nFq0r8MDe-y-cF2aWq6Qy9P_K-4=w300", isFolder=False)
	CategoryOrdem("cOrdFO")
	try:
		pagina=eval(pagina2)
		l= int(pagina)*5
		p= 1
		if int(pagina) > 0:
			AddDir("[COLOR blue][B]<< Pagina Anterior ["+ str( int(pagina) ) +"[/B]][/COLOR]", pagina , 120 ,"http://icons.iconarchive.com/icons/iconsmind/outline/256/Previous-icon.png", isFolder=False, background=pagina2)
		for x in range(0, 5):
			l +=1
			ordem = "asc" if cOrdFO=="title" else "desc"
			link = common.OpenURL("https://filmesonline.online/index.php?do=search&subaction=search&search_start="+str(l)+"&story="+urlfo+"&sortby="+cOrdFO+"&resorder="+ordem+"&catlist[]="+Clistafo0[int(Catfo)]).replace("\r","").replace("\n","")
			link = re.sub('Novos Filmes.+', '', link)
			m = re.compile('src=\"(.upload[^\"]+).+?alt=\"([^\"]+).+?href=\"([^\"]+)').findall(link)
			m2 = re.compile('numb-serial..(.+?)\<.+?afd..(\d+)').findall(link)
			i=0
			if m:
				#xbmcgui.Dialog().ok('Cube Play', str(m))
				for img2,name2,url2 in m:
					AddDir(name2 + " ("+m2[i][0]+") - " + m2[i][1], url2, 171, "https://filmesonline.online/"+img2, "https://filmesonline.online/"+img2, info="", background=url)
					p+=1
					i+=1
		if p >= 80:
			AddDir("[COLOR blue][B]Proxima Pagina >> ["+ str( int(pagina) + 2) +"[/B]][/COLOR]", pagina , 110 ,"http://icons.iconarchive.com/icons/iconsmind/outline/256/Next-2-2-icon.png", isFolder=False, background=pagina2)
	except urllib2.URLError, e:
		AddDir("Server error, tente novamente em alguns minutos" , "", 0, "", "")
		
def PlayMFO1(): #172
	if re.compile('\d+').findall(str ( background )) :
		s = background.split(",")
		sel = xbmcgui.Dialog().select("Selecione a resolução", s)
		if sel!=-1:
			link = common.OpenURL( url+"?q="+s[sel] )
			m = re.compile('https[^\"]+\.mp4').findall(link)
			global background
			background="None"
			PlayUrl(name, m[0],"",info)
	else:
		link = common.OpenURL(url)
		m = re.compile('https[^\"]+\.mp4').findall(link)
		background = "None"
		PlayUrl(name, m[0],"",info)
		
def GetMFO1(): #171
	try:
		link = common.OpenURL( url )
		m = re.compile('href\=\"(.+?\#Rapid)').findall(link)
		t = re.compile('class=\"titleblock\"\>\s\<h1\>([^\<]+)').findall(link)
		i = re.compile('class=\"p-info-text\"\>\s\<span\>([^\<]+)').findall(link)
		if m:
			link2 = common.OpenURL( "https://filmesonline.online"+m[0] )
			m2 = re.compile('iframe.+?src\=\"([^\"]+)').findall(link2)
			if m2:
				title = t[0] if t else name
				info = i[0] if i else ""
				link3 = common.OpenURL( "https:"+m2[0] )
				m3 = re.compile('https[^\"]+\.mp4').findall(link3)
				if m3:
					pp = re.compile('q=(\d+p)').findall(link3)
					pp = list(reversed(pp))
					AddDir( title , "https:"+m2[0], 172, iconimage, iconimage, isFolder=False, IsPlayable=True, info=info, background= ",".join(pp))
					AddDir( "Resoluções: "+", ".join(pp), "https:"+m2[0], 0, iconimage, iconimage, isFolder=False, info="Clique no título do filme para dar play")
				else:
					AddDir( "Video offline!!" ,"", 0, "", "", isFolder=False)
	except urllib2.URLError, e:
		AddDir( "Video offline" ,"", 0, "", "", isFolder=False)
# ----------------- FIM Filmes Online
# ----------------- Inicio MM filmes
def GenerosMM(): #189
	d = xbmcgui.Dialog().select("Escolha o Genero", ClistaMM1)
	if d != -1:
		global Cat
		Addon.setSetting("CatMM", str(d) )
		Cat = d
		Addon.setSetting("cPageMMf", "0" )
		xbmc.executebuiltin("XBMC.Container.Refresh()")
def ListFilmeLancMM(): #184
	l=0
	i=0
	try:
		links = common.OpenURL("http://www.mmfilmes.tv/series/")
		ms = re.compile('href\=\"(.+www.mmfilmes.tv.+)\" rel\=\"bookmark\"').findall(links)
		for x in range(0, 5):
			l+=1
			link = common.OpenURL("http://www.mmfilmes.tv/ultimos/page/"+str(l)+"/")
			m = re.compile('id\=\"post\-\d+\".+?\=.([^\"]+)\h*(?s)(.+?)(http[^\"]+)').findall(link)
			res = re.compile('audioy..([^\<]*)').findall(link)
			jpg = re.compile('src=\"(http.+?www.mmfilmes.tv\/wp-content\/uploads[^\"]+)').findall(link)
			dubleg = re.compile('boxxer.+\s.+boxxer..([^\<]*)').findall(link)
			if m:
				for name2,b,url2 in m:
					name2 = name2.replace("&#8211;","-").replace("&#038;","&").replace("&#8217;","\'")
					if not url2 in ms:
						AddDir(name2+ " [COLOR yellow]"+res[i]+"[/COLOR] [COLOR blue]"+dubleg[i]+"[/COLOR]", url2, 181, jpg[i], jpg[i],isFolder=True,IsPlayable=False)
					i+=1
			i=0
	except:
		pass
def ListFilmeMM(pagina2): #180
	AddDir("[COLOR yellow][B][Gênero dos Filmes]:[/B] " + ClistaMM1[int(CatMM)] +"[/COLOR]", "url" ,189 ,"https://lh5.ggpht.com/gv992ET6R_InCoMXXwIbdRLJczqOHFfLxIeY-bN2nFq0r8MDe-y-cF2aWq6Qy9P_K-4=w300", "https://lh5.ggpht.com/gv992ET6R_InCoMXXwIbdRLJczqOHFfLxIeY-bN2nFq0r8MDe-y-cF2aWq6Qy9P_K-4=w300", isFolder=False)
	pagina=eval(pagina2)
	l= int(pagina)*5
	p=1
	i=0
	if int(pagina) > 0:
		AddDir("[COLOR blue][B]<< Pagina Anterior ["+ str( int(pagina) ) +"[/B]][/COLOR]", pagina , 120 ,"http://icons.iconarchive.com/icons/iconsmind/outline/256/Previous-icon.png", isFolder=False, background=pagina2)
	try:
		links = common.OpenURL("http://www.mmfilmes.tv/series/")
		ms = re.compile('href\=\"(.+www.mmfilmes.tv.+)\" rel\=\"bookmark\"').findall(links)
		for x in range(0, 5):
			l+=1
			link = common.OpenURL("http://www.mmfilmes.tv/category/"+ ClistaMM0[int(CatMM)] +"/page/"+str(l)+"/")
			m = re.compile('id\=\"post\-\d+\".+?\=.([^\"]+)\h*(?s)(.+?)(http[^\"]+)').findall(link)
			res = re.compile('audioy..([^\<]*)').findall(link)
			jpg = re.compile('src=\"(http.+?www.mmfilmes.tv\/wp-content\/uploads[^\"]+)').findall(link)
			dubleg = re.compile('boxxer.+\s.+boxxer..([^\<]*)').findall(link)
			if m:
				for name2,b,url2 in m:
					name2 = name2.replace("&#8211;","-").replace("&#038;","&").replace("&#8217;","\'")
					if not url2 in ms:
						AddDir(name2+ " [COLOR yellow]"+res[i]+"[/COLOR] [COLOR blue]"+dubleg[i]+"[/COLOR]", url2, 181, jpg[i], jpg[i],isFolder=True,IsPlayable=False)
					i+=1
					p+=1
			i=0
			if p >= 50:
				AddDir("[COLOR blue][B]Proxima Pagina >> ["+ str( int(pagina) + 2) +"[/B]][/COLOR]", pagina , 110 ,"http://icons.iconarchive.com/icons/iconsmind/outline/256/Next-2-2-icon.png", isFolder=False, background=pagina2)
	except:
		pass
def OpenLinkMM(): #181
	link = common.OpenURL(url)
	m = re.compile('boxp\(.([^\']+)').findall(link)
	info2 = re.compile('mCSB_container..\s(\h*(?s)(.+?))\<\/div').findall(link)
	info2= info2[0][0].replace("\t","") if info2 else ""
	if m:
		link2 = common.OpenURL(m[0],headers={'referer': "http://www.mmfilmes.tv/"})
		m2 = re.compile('opb\(.([^\']+).+?.{3}.+?[^\\>]+.([^\<]+)').findall(link2)
		if m2:
			name2 = re.sub(' \[.+', '', name )
			for link,dubleg in m2:
				AddDir( name2 +" [COLOR blue]("+dubleg+")[/COLOR]" ,link, 182, iconimage, iconimage, isFolder=False, IsPlayable=True, info=info2, background=url)
def PlayLinkMM(): #182
	link = common.OpenURL(url,headers={'referer': "http://www.mmfilmes.tv/"})
	m = re.compile('addiframe\(\'([^\']+)').findall(link)
	if m:
		m[0] = "http://player.mmfilmes.tv" + m[0] if not "http" in m[0] else m[0]
		link2 = common.OpenURL(m[0],headers={'referer': "http://player.mmfilmes.tv"}).replace("file","\nfile")
		m2 = re.compile('file.+?(h[^\']+).+?(\d+p)\'').findall(link2)
		legenda = re.compile('([^\']+\.(vtt|srt|sub|ssa|txt|ass))').findall(link2)
		listar=[]
		listal=[]
		for link,res in m2:
			listal.append(link)
			listar.append(res)
		if len(listal) <1:
			xbmcgui.Dialog().ok('Cube Play', 'Erro, video não encontrado')
			sys.exit(int(sys.argv[1]))
		d = xbmcgui.Dialog().select("Selecione a resolução", listar)
		if d!= -1:
			url2 = re.sub(' ', '%20', listal[d] )
			global background
			background=background+";;;"+name+";;;MM"
			if legenda:
				legenda = re.sub(' ', '%20', legenda[0][0] )
				if not "http" in legenda:
					legenda = "http://player.mmfilmes.tv/" + legenda
				PlayUrl(name, url2, iconimage, info, sub=legenda)
			else:
				PlayUrl(name, url2, iconimage, info)
# -----------------
def ListSerieMM(): #190
	try:
		link = common.OpenURL("http://www.mmfilmes.tv/series/")
		m = re.compile('id\=\"post\-\d+\".+?\=.([^\"]+)\h*(?s)(.+?)(http[^\"]+)').findall(link)
		jpg = re.compile('src=\"(http.+?www.mmfilmes.tv\/wp-content\/uploads[^\"]+)').findall(link)
		i=0
		m2=[]
		if m:
			for name2,b,url2 in m:
				m2.append([name2,url2,jpg[i]])
				i+=1
			m2 = sorted(m2, key=lambda m2: m2[0])
			for name2,url2,jpg2 in m2:
				name2 = name2.replace("&#8211;","-").replace("&#038;","&").replace("&#8217;","\'")
				AddDir(name2, url2, 191, jpg2, jpg2, isFolder=True,IsPlayable=False)
	except:
		AddDir( "Server offline" ,"", 0, "", "", isFolder=False)
def ListSMM(x): #191
	link = common.OpenURL(url)
	m = re.compile('boxp\(.([^\']+)').findall(link)
	info2= re.compile('mCSB_container..\s(\h*(?s)(.+?))\<\/div').findall(link)
	info2= info2[0][0].replace("\t","") if info2 else ""
	i=0
	if m:
		if x=="None":
			link2 = common.OpenURL(m[0],headers={'referer': "http://www.mmfilmes.tv/"})
			m2 = re.compile('opb\(.([^\']+).+?.{3}.+?[^\\>]+.([^\<]+)').findall(link2)
			listar=[]
			listal=[]
			for link,res in m2:
				listal.append(link)
				listar.append(res)
			if len(listar)==1:
				d=0
			else:
				d = xbmcgui.Dialog().select("Selecione o server:", listar)
			if d== -1:
				d= 0
			if m2:
				link3 = common.OpenURL(m2[0][0],headers={'referer': "http://www.mmfilmes.tv/"}).replace("\n","").replace("\r","").replace('".Svplayer"',"<end>").replace('\t'," ")
				link3 = re.sub('(\(s \=\= \d+\))', r'<end>\1', link3 )
				m3 = re.compile('s \=\= (\d+)(.+?\<end\>)').findall(link3)
				for temp in m3:
					AddDir("[B][Temporada "+ temp[0] +"][/B]" ,listal[d], 192, iconimage, iconimage, isFolder=True, info=info2, background=i)
					i+=1
def ListEpiMM(x): #192
	link3 = common.OpenURL(url,headers={'referer': "http://www.mmfilmes.tv/"}).replace("\n","").replace("\r","").replace('".Svplayer"',"<end>").replace('\t'," ")
	link3 = re.sub('(\(s \=\= \d+\))', r'<end>\1', link3 )
	m3 = re.compile('s \=\= (\d+)(.+?\<end\>)').findall(link3)
	r=-1
	p=1
	dubleg = re.compile("t \=\= \'([^\']+)(.+?\})").findall( m3[int(x)][1] )
	epi = re.compile("e \=\= (\d+).+?addiframe\(\'([^\']+)").findall( m3[int(x)][1] )
	for e,url2 in epi:
		url2 = "http://player.mmfilmes.tv" + url2 if not "http" in url2 else url2
		if p == int(e) :
			r+=1
		if len(dubleg[r][1]) < 30:
			r+=1
		name2 = "[COLOR yellow](Dub)[/COLOR]" if "dub" in dubleg[r][0] else "[COLOR blue](Leg)[/COLOR]"
		AddDir("Episódio "+ e + " [COLOR blue]" + name2 ,url2, 194, iconimage, iconimage, isFolder=False, IsPlayable=True, info=info)
def PlaySMM(): #194
	if "drive.google" in url:
		xbmcgui.Dialog().ok('Cube Play', 'Erro, video não encontrado')
		sys.exit()
	link2 = common.OpenURL(url,headers={'referer': "http://player.mmfilmes.tv"}).replace('"',"'")
	m2 = re.compile('(h[^\']+).+?label...(\w+)').findall(link2)
	legenda = re.compile('([^\']+\.(vtt|srt|sub|ssa|txt|ass))').findall(link2)
	listar=[]
	listal=[]
	for link,res in m2:
		listal.append(link)
		listar.append(res)
	if len(listal) < 1:
		xbmcgui.Dialog().ok('Cube Play', 'Erro, video não encontrado')
		sys.exit(int(sys.argv[1]))
	d = xbmcgui.Dialog().select("Selecione a resolução", listar)
	if d!= -1:
		url2 = re.sub(' ', '%20', listal[d] )
		if legenda:
			legenda = re.sub(' ', '%20', legenda[0][0] )
			if not "http" in legenda:
				legenda = "http://player.mmfilmes.tv/" + legenda
			PlayUrl(name, url2, iconimage, info, sub=legenda)
		else:
			PlayUrl(name, url2, iconimage, info)
# ----------------- Fim MM filmes
# ----------------- Inicio Go Filmes
def GenerosGO(): #219
	d = xbmcgui.Dialog().select("Escolha o Genero", ClistaGO1)
	if d != -1:
		global Cat
		Addon.setSetting("CatGO", str(d) )
		Cat = d
		Addon.setSetting("cPageGOf", "0" )
		xbmc.executebuiltin("XBMC.Container.Refresh()")
def ListGO(pagina2): #210
	AddDir("[COLOR yellow][B][Gênero dos Filmes]:[/B] " + ClistaGO1[int(CatGO)] +"[/COLOR]", "url" ,219 ,"https://lh5.ggpht.com/gv992ET6R_InCoMXXwIbdRLJczqOHFfLxIeY-bN2nFq0r8MDe-y-cF2aWq6Qy9P_K-4=w300", "https://lh5.ggpht.com/gv992ET6R_InCoMXXwIbdRLJczqOHFfLxIeY-bN2nFq0r8MDe-y-cF2aWq6Qy9P_K-4=w300", isFolder=False)
	pagina=eval(pagina2)
	l= int(pagina)*5
	p=1
	i=0
	if int(pagina) > 0:
		AddDir("[COLOR blue][B]<< Pagina Anterior ["+ str( int(pagina) ) +"[/B]][/COLOR]", pagina , 120 ,"http://icons.iconarchive.com/icons/iconsmind/outline/256/Previous-icon.png", isFolder=False, background=pagina2)
	try:
		for x in range(0, 5):
			l+=1
			if ClistaGO0[int(CatGO)] == "all":
				link = common.OpenURL("http://gofilmes.me/?p="+str(l)).replace("</div></div>","\r\n")
			else:
				link = common.OpenURL("http://gofilmes.me/genero/"+ClistaGO0[int(CatGO)]+"?p="+str(l)).replace("</div></div>","\r\n")
			m = re.compile('href=\"([^\"]+)\" title\=\"([^\"]+).+b\" src\=\"([^\"]+).+n\">([^\<]+)').findall(link)
			for url2,name2,img2,info2 in m:
				try:
					info2= re.sub('&([^;]+);', lambda m: unichr(htmlentitydefs.name2codepoint[m.group(1)]), info2).encode('utf-8')
				except:
					pass
				name2 = name2.replace("Assistir ","").replace(" Online"," -")
				AddDir(name2, url2, 211, img2, img2, isFolder=False, IsPlayable=True, info=info2)
				p+=1
		if p >= 120:
			AddDir("[COLOR blue][B]Proxima Pagina >> ["+ str( int(pagina) + 2) +"[/B]][/COLOR]", pagina , 110 ,"http://icons.iconarchive.com/icons/iconsmind/outline/256/Next-2-2-icon.png", isFolder=False, background=pagina2)
	except:
		AddDir( "Server offline" ,"", 0, "", "", isFolder=False)
def PlayGO(): #211
	try:
		link = common.OpenURL(url)
		m = re.compile('iframe src\="([^\"]+)').findall(link)
		link2 = common.OpenURL(m[0])
		m2 = re.compile('href=\"([^\"]+)\".+?\"\>([^\<]+)').findall(link2)
		listu=[]
		listn=[]
		i=0
		for url3,dl3 in m2:
			link3 = common.OpenURL("http://sokodi.net/play/moon.php?url="+url3)
			m3 = re.compile('\=(.+?x[^,]+).+\s(.+)').findall(link3)
			m3 = sorted(m3, key=lambda m3: m3[0])
			for res4,url4 in m3:
				listn.append("[COLOR blue]"+ m2[i][1] +"[/COLOR] " + "[COLOR yellow]"+ res4 +"[/COLOR]")
				listu.append(url4)
			i+=1
		if len(listn) >=1:
			d = xbmcgui.Dialog().select("Selecione a resolução", listn)
			if d!= -1:
				PlayUrl(name, listu[d], iconimage, info)
		else:
			xbmcgui.Dialog().ok("Cube Play", "Não foi possível carregar o vídeo")
	except:
		xbmcgui.Dialog().ok("Cube Play", "Não foi possível carregar o vídeo")
# ----------------- Fim Go Filmes
def GetChoice(choiceTitle, fileTitle, urlTitle, choiceFile, choiceUrl, choiceNone=None, fileType=1, fileMask=None, defaultText=""):
	choice = ''
	choiceList = [getLocaleString(choiceFile), getLocaleString(choiceUrl)]
	if choiceNone is not None:
		choiceList = [getLocaleString(choiceNone)] + choiceList
	method = GetSourceLocation(getLocaleString(choiceTitle), choiceList)	
	if choiceNone is None and method == 0 or choiceNone is not None and method == 1:
		if not defaultText.startswith('http'):
			defaultText = ""
		choice = GetKeyboardText(getLocaleString(fileTitle), defaultText).strip().decode("utf-8")
	elif choiceNone is None and method == 1 or choiceNone is not None and method == 2:
		if defaultText.startswith('http'):
			defaultText = ""
		choice = xbmcgui.Dialog().browse(fileType, getLocaleString(urlTitle), 'files', fileMask, False, False, defaultText).decode("utf-8")
	return choice			
def PlayUrl(name, url, iconimage=None, info='', sub='', metah=''):
	if ";;;" in background:
		b = background.split(";;;")
		if "RC" in b[2]:
			AddFavorites(b[0], iconimage, b[1], "95", "historic.txt")
		elif "NC" in b[2]:
			AddFavorites(b[0], iconimage, b[1], "78", "historic.txt")
		elif "MM" in b[2]:
			AddFavorites(b[0], iconimage, b[1], "181", "historic.txt")
	url = re.sub('\.mp4$', '.mp4?play', url)
	url = common.getFinalUrl(url)
	#xbmc.log('--- Playing "{0}". {1}'.format(name, url), 2)
	listitem = xbmcgui.ListItem(path=url)
	if metah:
		listitem.setInfo(type="Video", infoLabels=metah)
	else:
		listitem.setInfo(type="Video", infoLabels={"mediatype": "video", "Title": name, "Plot": info })
	if sub!='':
		listitem.setSubtitles(['special://temp/example.srt', sub ])
	if iconimage is not None:
		try:
			listitem.setArt({'thumb' : iconimage})
		except:
			listitem.setThumbnailImage(iconimage)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)

def AddDir(name, url, mode, iconimage='', logos='', index=-1, move=0, isFolder=True, IsPlayable=False, background=None, cacheMin='0', info='', metah=''):
	urlParams = {'name': name, 'url': url, 'mode': mode, 'iconimage': iconimage, 'logos': logos, 'cache': cacheMin, 'info': info, 'background': background, 'metah': metah}
	liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage )
	if metah:
		liz.setInfo(type="Video", infoLabels=metah)
		liz.setArt({"thumb": metah['cover_url'], "poster": metah['cover_url'], "banner": metah['cover_url'], "fanart": metah['backdrop_url'] })
	else:
		liz.setInfo(type="Video", infoLabels={ "Title": name, "Plot": info })
		#liz.setProperty("Fanart_Image", logos)
		liz.setArt({"poster": iconimage, "banner": logos, "fanart": logos })
	#listMode = 21 # Lists
	if IsPlayable:
		liz.setProperty('IsPlayable', 'true')
	items = []
	if mode == 1 or mode == 2:
		items = []
	elif mode== 61 and info=="":
		liz.addContextMenuItems(items = [("Add ao fav. do Cube Play", 'XBMC.RunPlugin({0}?url={1}&mode=31&iconimage={2}&name={3})'.format(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(iconimage), urllib.quote_plus(name)))])
	elif mode== 78:
		liz.addContextMenuItems(items = [("Add ao fav. do Cube Play", 'XBMC.RunPlugin({0}?url={1}&mode=72&iconimage={2}&name={3})'.format(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(iconimage), urllib.quote_plus(name)))])
	elif mode== 95:
		liz.addContextMenuItems(items = [("Add ao fav. do Cube Play", 'XBMC.RunPlugin({0}?url={1}&mode=93&iconimage={2}&name={3})'.format(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(iconimage), urllib.quote_plus(name)))])
	elif mode== 135:
		liz.addContextMenuItems(items = [("Add ao fav. do Cube Play", 'XBMC.RunPlugin({0}?url={1}&mode=131&iconimage={2}&name={3})'.format(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(iconimage), urllib.quote_plus(name)))])
	elif mode== 171:
		liz.addContextMenuItems(items = [("Add ao fav. do Cube Play", 'XBMC.RunPlugin({0}?url={1}&mode=175&iconimage={2}&name={3})'.format(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(iconimage), urllib.quote_plus(name)))])
	elif mode== 181:
		liz.addContextMenuItems(items = [("Add ao fav. do Cube Play", 'XBMC.RunPlugin({0}?url={1}&mode=185&iconimage={2}&name={3})'.format(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(iconimage), urllib.quote_plus(name)))])
	elif mode== 191:
		liz.addContextMenuItems(items = [("Add ao fav. do Cube Play", 'XBMC.RunPlugin({0}?url={1}&mode=195&iconimage={2}&name={3})'.format(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(iconimage), urllib.quote_plus(name)))])
	if info=="Filmes Favoritos":
		items = [("Remover dos favoritos", 'XBMC.RunPlugin({0}?index={1}&mode=333)'.format(sys.argv[0], index)),
		(getLocaleString(30030), 'XBMC.RunPlugin({0}?index={1}&mode={2}&move=-1)'.format(sys.argv[0], index, 338)),
		(getLocaleString(30031), 'XBMC.RunPlugin({0}?index={1}&mode={2}&move=1)'.format(sys.argv[0], index, 338)),
		(getLocaleString(30032), 'XBMC.RunPlugin({0}?index={1}&mode={2}&move=0)'.format(sys.argv[0], index, 338))]
		liz.addContextMenuItems(items)
	if info=="Séries Favoritas":
		items = [("Remover dos favoritos", 'XBMC.RunPlugin({0}?index={1}&mode=334)'.format(sys.argv[0], index)),
		(getLocaleString(30030), 'XBMC.RunPlugin({0}?index={1}&mode={2}&move=-1)'.format(sys.argv[0], index, 339)),
		(getLocaleString(30031), 'XBMC.RunPlugin({0}?index={1}&mode={2}&move=1)'.format(sys.argv[0], index, 339)),
		(getLocaleString(30032), 'XBMC.RunPlugin({0}?index={1}&mode={2}&move=0)'.format(sys.argv[0], index, 339))]
		liz.addContextMenuItems(items)
	if mode == 10:
		urlParams['index'] = index
	u = '{0}?{1}'.format(sys.argv[0], urllib.urlencode(urlParams))
	xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=isFolder)

def GetKeyboardText(title = "", defaultText = ""):
	keyboard = xbmc.Keyboard(defaultText, title)
	keyboard.doModal()
	text = "" if not keyboard.isConfirmed() else keyboard.getText()
	return text

def GetSourceLocation(title, chList):
	dialog = xbmcgui.Dialog()
	answer = dialog.select(title, chList)
	return answer
	
def AddFavorites(url, iconimage, name, mode, file):
	file = os.path.join(addon_data_dir, file)
	favList = common.ReadList(file)
	for item in favList:
		if item["url"].lower() == url.decode("utf-8").lower():
			if "favorites" in file:
				xbmc.executebuiltin("Notification({0}, '{1}' {2}, 5000, {3})".format(AddonName, name, getLocaleString(30011), icon))
			return
	chList = []	
	for channel in chList:
		if channel["name"].lower() == name.decode("utf-8").lower():
			url = channel["url"].encode("utf-8")
			iconimage = channel["image"].encode("utf-8")
			break
	if not iconimage:
		iconimage = ""
	data = {"url": url.decode("utf-8"), "image": iconimage.decode("utf-8"), "name": name.decode("utf-8"), "mode": mode}
	favList.append(data)
	common.SaveList(file, favList)
	if "favorites" in file:
		xbmc.executebuiltin("Notification({0}, '{1}' {2}, 5000, {3})".format(AddonName, name, getLocaleString(30012), icon))
	
def ListFavorites(file, info):
	file = os.path.join(addon_data_dir, file)
	chList = common.ReadList(file)
	i = 0
	for channel in chList:
		AddDir(channel["name"].encode("utf-8"), channel["url"].encode("utf-8"), channel["mode"], channel["image"].encode("utf-8"), channel["image"].encode("utf-8"), index=i, isFolder=True, IsPlayable=False, info=info)
		i += 1
		
def ListHistoric(file, info):
	file = os.path.join(addon_data_dir, file)
	chList = common.ReadList(file)
	for channel in reversed(chList):
		AddDir(channel["name"].encode("utf-8"), channel["url"].encode("utf-8"), channel["mode"], channel["image"].encode("utf-8"), channel["image"].encode("utf-8"), isFolder=True, IsPlayable=False, info=info)

def RemoveFromLists(index, listFile):
	chList = common.ReadList(listFile) 
	if index < 0 or index >= len(chList):
		return
	del chList[index]
	common.SaveList(listFile, chList)
	xbmc.executebuiltin("XBMC.Container.Refresh()")
		
def AddNewFavorite(file):
	file = os.path.join(addon_data_dir, file)
	chName = GetKeyboardText(getLocaleString(30014))
	if len(chName) < 1:
		return
	chUrl = GetKeyboardText(getLocaleString(30015))
	if len(chUrl) < 1:
		return
	image = GetChoice(30023, 30023, 30023, 30024, 30025, 30021, fileType=2)
		
	favList = common.ReadList(file)
	for item in favList:
		if item["url"].lower() == chUrl.decode("utf-8").lower():
			xbmc.executebuiltin("Notification({0}, '{1}' {2}, 5000, {3})".format(AddonName, chName, getLocaleString(30011), icon))
			return			
	data = {"url": chUrl.decode("utf-8"), "image": image, "name": chName.decode("utf-8")}	
	favList.append(data)
	if common.SaveList(file, favList):
		xbmc.executebuiltin("XBMC.Container.Refresh()")
	
def MoveInList(index, step, listFile):
	theList = common.ReadList(listFile)
	if index + step >= len(theList) or index + step < 0:
		return
	if step == 0:
		step = GetIndexFromUser(len(theList), index)
	if step < 0:
		tempList = theList[0:index + step] + [theList[index]] + theList[index + step:index] + theList[index + 1:]
	elif step > 0:
		tempList = theList[0:index] + theList[index +  1:index + 1 + step] + [theList[index]] + theList[index + 1 + step:]
	else:
		return
	common.SaveList(listFile, tempList)
	xbmc.executebuiltin("XBMC.Container.Refresh()")

def GetNumFromUser(title, defaultt=''):
	dialog = xbmcgui.Dialog()
	choice = dialog.input(title, defaultt=defaultt, type=xbmcgui.INPUT_NUMERIC)
	return None if choice == '' else int(choice)

def GetIndexFromUser(listLen, index):
	dialog = xbmcgui.Dialog()
	location = GetNumFromUser('{0} (1-{1})'.format(getLocaleString(30033), listLen))
	return 0 if location is None or location > listLen or location <= 0 else location - 1 - index

def Refresh():
	xbmc.executebuiltin("XBMC.Container.Refresh()")

def TogglePrevious(url, background):
	Addon.setSetting(background, str(int(url) - 1) )
	xbmc.executebuiltin("XBMC.Container.Refresh()")

def ToggleNext(url, background):
	#xbmcgui.Dialog().ok('Cube Play', url + " " +background)
	Addon.setSetting(background, str(int(url) + 1) )
	xbmc.executebuiltin("XBMC.Container.Refresh()")

def getmd5(t):
	value_altered = ''.join(chr(ord(letter)-1) for letter in t)
	return value_altered

def CheckUpdate(msg): #200
	try:
		uversao = urllib2.urlopen( "https://raw.githubusercontent.com/D4anielCB/CB/master/version.txt" ).read().replace('\n','').replace('\r','')
		uversao = re.compile('[a-zA-Z\.\d]+').findall(uversao)[0]
		#xbmcgui.Dialog().ok(Versao, uversao)
		if uversao != Versao:
			Update()
			xbmc.executebuiltin("XBMC.Container.Refresh()")
		elif msg==True:
			xbmcgui.Dialog().ok('Cube Play', "O addon já esta na última versao: "+Versao+"\nAs atualizações normalmente são automáticas\nUse esse recurso caso nao esteja recebendo automaticamente")
			xbmc.executebuiltin("XBMC.Container.Refresh()")
	except urllib2.URLError, e:
		if msg==True:
			xbmcgui.Dialog().ok('Cube Play', "Não foi possível checar")

def Update():
	Path = xbmc.translatePath( xbmcaddon.Addon().getAddonInfo('path') ).decode("utf-8")
	try:
		fonte = urllib2.urlopen( "https://raw.githubusercontent.com/D4anielCB/CB/master/default.py" ).read().replace('\n','')
		prog = re.compile('#checkintegrity25852').findall(fonte)
		if prog:
			py = os.path.join( Path, "default.py")
			file = open(py, "w")
			file.write(fonte)
			file.close()
		fonte = urllib2.urlopen( "https://raw.githubusercontent.com/D4anielCB/CB/master/resources/settings.xml" ).read().replace('\n','')
		prog = re.compile('</settings>').findall(fonte)
		if prog:
			py = os.path.join( Path, "resources/settings.xml")
			file = open(py, "w")
			file.write(fonte)
			file.close()
		fonte = urllib2.urlopen( "https://raw.githubusercontent.com/D4anielCB/CB/master/addon.xml" ).read().replace('\n','')
		prog = re.compile('</addon>').findall(fonte)
		if prog:
			py = os.path.join( Path, "addon.xml")
			file = open(py, "w")
			file.write(fonte)
			file.close()
		xbmc.executebuiltin("Notification({0}, {1}, 9000, {2})".format(AddonName, "Atualizando o addon. Aguarde um momento!", icon))
		xbmc.sleep(2000)
	except:
		xbmcgui.Dialog().ok('Cube Play', "Ocorreu um erro, tente novamente mais tarde")

def ST(x):
	x = str(x)
	Path = xbmc.translatePath( xbmcaddon.Addon().getAddonInfo('path') ).decode("utf-8")
	py = os.path.join( Path, "study.txt")
	file = open(py, "w")
	file.write(x)
	file.close()

params = dict(urlparse.parse_qsl(sys.argv[2].replace('?','')))
url = params.get('url')
logos = params.get('logos', '')
name = params.get('name')
iconimage = params.get('iconimage')
cache = int(params.get('cache', '0'))
index = int(params.get('index', '-1'))
move = int(params.get('move', '0'))
mode = int(params.get('mode', '0'))
info = params.get('info')
background = params.get('background')
metah = params.get('metah')

if mode == 0:
	Categories()
	setViewM()
	if cadulto!="update":
		CheckUpdate(False)	
elif mode == -1: MCanais()
elif mode == -2: MFilmes()
elif mode == -3: MSeries()
elif mode == 3 or mode == 32:
	PlayUrl(name, url, iconimage, info)
elif mode == 301:
	ListFavorites('favoritesf.txt', "Filmes Favoritos")
	setViewS()
elif mode == 302:
	ListFavorites('favoritess.txt', "Séries Favoritas")
	setViewM()
elif mode == 305:
	ListHistoric('historic.txt', "Historico")
	setViewM()
elif mode == 31: 
	AddFavorites(url, iconimage, name, "61", 'favoritess.txt')
elif mode == 72: 
	AddFavorites(url, iconimage, name, "78", 'favoritesf.txt')
elif mode == 93: 
	AddFavorites(url, iconimage, name, "95", 'favoritesf.txt')
elif mode == 131: 
	AddFavorites(url, iconimage, name, "135", 'favoritess.txt')
elif mode == 175: 
	AddFavorites(url, iconimage, name, "171", 'favoritesf.txt')
elif mode == 185: 
	AddFavorites(url, iconimage, name, "181", 'favoritesf.txt')
elif mode == 195: 
	AddFavorites(url, iconimage, name, "191", 'favoritess.txt')
elif mode == 333:
	RemoveFromLists(index, favfilmesFile)
elif mode == 338:
	MoveInList(index, move, favfilmesFile)
elif mode == 334:
	RemoveFromLists(index, favseriesFile)
elif mode == 339:
	MoveInList(index, move, favseriesFile)
elif mode == 38:
	dialog = xbmcgui.Dialog()
	ret = dialog.yesno('Cube Play', 'Deseja mesmo deletar todos os filmes favoritos?')
	if ret:
		common.DelFile(favfilmesFile)
		sys.exit()
elif mode == 39:
	dialog = xbmcgui.Dialog()
	ret = dialog.yesno('Cube Play', 'Deseja mesmo deletar todos os seriados favoritos?')
	if ret:
		common.DelFile(favseriesFile)
		sys.exit()
elif mode == 40:
	dialog = xbmcgui.Dialog()
	ret = dialog.yesno('Cube Play', 'Deseja mesmo deletar todo o historico?')
	if ret:
		common.DelFile(historicFile)
		sys.exit()
elif mode == 50:
	Refresh()
elif mode == 60:
	Series()
	setViewS()
elif mode == 61:
	ListSNC(background)
	setViewS()
elif mode == 62:
	PlayS()
	setViewS()
elif mode == 71:
	MoviesNC()
	setViewM()
elif mode == 78:
	ListMoviesNC()
	setViewS()
elif mode == 79:
	PlayMNC()
	setViewS()
elif mode == 80:
	Generos()
elif mode == 81:
	CategoryOrdem2(url)
elif mode == 90:
	MoviesRCD()
	setViewM()
elif mode == 91:
	MoviesRCL()
	setViewM()
elif mode == 92:
	MoviesRCN()
	setViewM()
elif mode == 95:
	PlayMRC()
	setViewM()
elif mode == 100:
	TVRC()
	setViewM()
elif mode == 101:
	PlayTVRC()
elif mode == 102:
	TVCB(url)
	setViewM()
elif mode == 103:
	PlayTVCB()
elif mode == 105:
	Addon.setSetting("cEPG", "1")
	xbmc.executebuiltin("XBMC.Container.Refresh()")
elif mode == 110:
	ToggleNext(url, background)
elif mode == 120:
	TogglePrevious(url, background)
elif mode == 130:
	SeriesRC("series","cPageser")
	setViewS()
elif mode == 135:
	TemporadasRC(background)
	setViewS()
elif mode == 133:
	PlaySRC()
	setViewS()
elif mode == 139:
	AllEpisodiosRC()
	setViewS()
elif mode == 140:
	SeriesRC("animes","cPageani")
	setViewS()
elif mode == 150:
	SeriesRC("desenhos","cPagedes")
	setViewS()
elif mode == 160:
	Busca()
	setViewM()
elif mode == 170:
	MoviesFO("Rapidvideo","cPagefo1")
	setViewM()
elif mode == 171:
	GetMFO1()
	setViewM()
elif mode == 172:
	PlayMFO1()
elif mode == 85:
	GenerosFO()
elif mode == 180:
	ListFilmeMM("cPageMMf")
	setViewM()
elif mode == 181:
	OpenLinkMM()
	setViewM()
elif mode == 182:
	PlayLinkMM()
elif mode == 184:
	ListFilmeLancMM()
	setViewM()
elif mode == 189:
	GenerosMM()
elif mode == 190:
	ListSerieMM()
	setViewS()
elif mode == 191:
	ListSMM(background)
	setViewS()
elif mode == 192:
	ListEpiMM(background)
	setViewS()
elif mode == 194:
	PlaySMM()
elif mode == 200:
	CheckUpdate(True)
elif mode == 210:
	ListGO("cPageGOf")
	setViewM()
elif mode == 211:
	PlayGO()
elif mode == 219:
	GenerosGO()
elif mode == 220:
	Filmes96()
elif mode == 221:
	MoviesRCR() ###
	setViewM()
elif mode == 229:
	PlayFilmes96()
	
xbmcplugin.endOfDirectory(int(sys.argv[1]))
#checkintegrity25852
