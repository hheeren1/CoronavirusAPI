import requests
import urllib.request
import time
import threading
import datetime
import codecs
import json
from urllib.request import urlopen
from json import load
from bs4 import BeautifulSoup
from flask import Flask, request
from flask import jsonify
from apscheduler.schedulers.background import BackgroundScheduler

countries = ['Andorra', 'UAE', 'Afghanistan', 'Antigua and Barbuda', 'Anguilla', 'Albania', 'Armenia', 'Angola', 'Antarctica', 'Argentina', 'American Samoa', 'Austria', 'Australia', 'Aruba', 'Åland Islands', 'Azerbaijan', 'Bosnia and Herzegovina', 'Barbados', 'Bangladesh', 'Belgium', 'Burkina Faso', 'Bulgaria', 'Bahrain', 'Burundi', 'Benin', 'Saint Barthélemy', 'Bermuda', 'Brunei Darussalam', 'Bolivia', 'Bonaire, Sint Eustatius and Saba', 'Brazil', 'Bahamas', 'Bhutan', 'Bouvet Island', 'Botswana', 'Belarus', 'Belize', 'Canada', 'Cocos (Keeling) Islands', 'DRC', 'cf', 'Congo', 'Switzerland', "Côte D'Ivoire", 'Cook Islands', 'Chile', 'Cameroon', 'China', 'Colombia', 'Costa Rica', 'Cuba', 'Cape Verde', 'Curaçao', 'Christmas Island', 'Cyprus', 'Czech Republic', 'Germany', 'Djibouti', 'Denmark', 'Dominica', 'Dominican Republic', 'Algeria', 'Ecuador', 'Estonia', 'Egypt', 'Western Sahara', 'Eritrea', 'Spain', 'Ethiopia', 'Finland', 'Fiji', 'Falkland Islands (Malvinas)', 'Micronesia', 'Faroe Islands', 'France', 'Gabon', 'UK', 'Grenada', 'Georgia', 'French Guiana', 'Guernsey', 'Ghana', 'Gibraltar', 'Greenland', 'Gambia', 'Guinea', 'Guadeloupe', 'Equatorial Guinea', 'Greece', 'South Georgia', 'Guatemala', 'Guam', 'Guinea-Bissau', 'Guyana', 'Hong Kong', 'Heard Island and Mcdonald Islands', 'Honduras', 'Croatia', 'Haiti', 'Hungary', 'Indonesia', 'Ireland', 'Israel', 'Isle of Man', 'India', 'British Indian Ocean Territory', 'Iraq', 'Iran', 'Iceland', 'Italy', 'Jersey', 'Jamaica', 'Jordan', 'Japan', 'Kenya', 'Kyrgyzstan', 'Cambodia', 'Kiribati', 'Comoros', 'Saint Kitts and Nevis', 'North Korea', 'S. Korea', 'Kuwait', 'Cayman Islands', 'Kazakhstan', "Lao People's Democratic Republic", 'Lebanon', 'Saint Lucia', 'Liechtenstein', 'Sri Lanka', 'Liberia', 'Lesotho', 'Lithuania', 'Luxembourg', 'Latvia', 'Libya', 'Morocco', 'Monaco', 'Moldova', 'Montenegro', 'Saint Martin (French Part)', 'Madagascar', 'Marshall Islands', 'Macedonia', 'Mali', 'Myanmar', 'Mongolia', 'Macao', 'Northern Mariana Islands', 'Martinique', 'Mauritania', 'Montserrat', 'Malta', 'Mauritius', 'Maldives', 'Malawi', 'Mexico', 'Malaysia', 'Mozambique', 'Namibia', 'New Caledonia', 'Niger', 'Norfolk Island', 'Nigeria', 'Nicaragua', 'Netherlands', 'Norway', 'Nepal', 'Nauru', 'Niue', 'New Zealand', 'Oman', 'Panama', 'Peru', 'French Polynesia', 'Papua New Guinea', 'Philippines', 'Pakistan', 'Poland', 'Saint Pierre and Miquelon', 'Pitcairn', 'Puerto Rico', 'Palestinian Territory', 'Portugal', 'Palau', 'Paraguay', 'Qatar', 'Réunion', 'Romania', 'Serbia', 'Russia', 'Rwanda', 'Saudi Arabia', 'Solomon Islands', 'Seychelles', 'Sudan', 'Sweden', 'Singapore', 'Saint Helena, Ascension and Tristan Da Cunha', 'Slovenia', 'Svalbard and Jan Mayen', 'Slovakia', 'Sierra Leone', 'San Marino', 'Senegal', 'Somalia', 'Suriname', 'South Sudan', 'Sao Tome and Principe', 'El Salvador', 'Sint Maarten (Dutch Part)', 'Syrian Arab Republic', 'Swaziland', 'Turks and Caicos Islands', 'Chad', 'French Southern Territories', 'Togo', 'Thailand', 'Tajikistan', 'Tokelau', 'Timor-Leste', 'Turkmenistan', 'Tunisia', 'Tonga', 'Turkey', 'Trinidad and Tobago', 'Tuvalu', 'Taiwan', 'Tanzania', 'Ukraine', 'Uganda', 'United States Minor Outlying Islands', 'USA', 'Uruguay', 'Uzbekistan', 'Vatican City', 'Saint Vincent and The Grenadines', 'Venezuela', 'Virgin Islands, British', 'Virgin Islands, U.S.', 'Viet Nam', 'Vanuatu', 'Wallis and Futuna', 'Samoa', 'Yemen', 'Mayotte', 'South Africa', 'Zambia', 'Zimbabwe', 'World']

flags = ["https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/ad.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/ae.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/af.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/ag.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/ai.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/al.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/am.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/ao.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/aq.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/ar.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/as.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/at.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/au.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/aw.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/ax.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/az.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/ba.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/bb.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/bd.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/be.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/bf.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/bg.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/bh.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/bi.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/bj.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/bl.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/bm.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/bn.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/bo.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/bq.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/br.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/bs.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/bt.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/bv.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/bw.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/by.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/bz.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/ca.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/cc.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/cd.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/cf.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/cg.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/ch.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/ci.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/ck.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/cl.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/cm.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/cn.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/co.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/cr.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/cu.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/cv.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/cw.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/cx.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/cy.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/cz.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/de.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/dj.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/dk.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/dm.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/do.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/dz.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/ec.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/ee.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/eg.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/eh.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/er.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/es.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/et.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/fi.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/fj.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/fk.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/fm.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/fo.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/fr.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/ga.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/gb.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/gd.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/ge.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/gf.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/gg.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/gh.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/gi.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/gl.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/gm.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/gn.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/gp.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/gq.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/gr.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/gs.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/gt.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/gu.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/gw.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/gy.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/hk.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/hm.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/hn.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/hr.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/ht.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/hu.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/id.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/ie.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/il.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/im.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/in.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/io.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/iq.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/ir.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/is.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/it.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/je.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/jm.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/jo.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/jp.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/ke.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/kg.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/kh.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/ki.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/km.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/kn.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/kp.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/kr.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/kw.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/ky.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/kz.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/la.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/lb.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/lc.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/li.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/lk.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/lr.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/ls.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/lt.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/lu.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/lv.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/ly.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/ma.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/mc.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/md.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/me.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/mf.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/mg.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/mh.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/mk.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/ml.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/mm.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/mn.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/mo.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/mp.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/mq.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/mr.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/ms.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/mt.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/mu.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/mv.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/mw.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/mx.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/my.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/mz.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/na.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/nc.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/ne.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/nf.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/ng.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/ni.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/nl.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/no.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/np.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/nr.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/nu.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/nz.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/om.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/pa.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/pe.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/pf.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/pg.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/ph.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/pk.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/pl.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/pm.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/pn.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/pr.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/ps.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/pt.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/pw.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/py.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/qa.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/re.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/ro.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/rs.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/ru.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/rw.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/sa.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/sb.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/sc.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/sd.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/se.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/sg.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/sh.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/si.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/sj.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/sk.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/sl.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/sm.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/sn.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/so.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/sr.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/ss.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/st.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/sv.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/sx.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/sy.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/sz.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/tc.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/td.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/tf.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/tg.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/th.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/tj.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/tk.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/tl.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/tm.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/tn.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/to.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/tr.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/tt.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/tv.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/tw.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/tz.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/ua.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/ug.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/um.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/us.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/uy.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/uz.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/va.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/vc.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/ve.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/vg.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/vi.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/vn.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/vu.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/wf.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/ws.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/ye.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/yt.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/za.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/zm.png", "https://raw.githubusercontent.com/hjnilsson/country-flags/master/png1000px/zw.png", "https://www.globe.gov/globe-gov-home-portlet/images/learn-earth-system/learn-earth-system-clean.png"]

#Initializing global variables
lastupdated = ""
alldata = []

def update():
    url = 'https://www.worldometers.info/coronavirus/'
    while True:
        response = requests.get(url)
        if response.status_code != 500:
            break
        else:
            time.sleep(5)
    soup = BeautifulSoup(response.text, "html.parser")
    for item in soup.select("div.content-inner"):
        global lastupdated
        lastupdated = item.find_all('div')[1].get_text()
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find('table', attrs={'id':'main_table_countries_today'})
    table_body = table.find('tbody')
    alltemp = []
    data = {}
    rows = table_body.findChildren('tr')
    for row in rows:
        cells = row.findChildren('td')
        index = 0
        for cell in cells:
            if cell.string == None and data == {}:
                break
            else:
                if index == 0:
                    data['Country'] = cell.string
                    index +=1
                elif index == 1:
                    data['Cases'] = cell.string
                    index +=1
                elif index == 2:
                    data['NewCases'] = cell.string
                    index +=1
                elif index == 3:
                    data['Deaths'] = cell.string
                    index +=1
                elif index == 4:
                    data['NewDeaths'] = cell.string
                    index +=1
                elif index == 5:
                    data['Recovered'] = cell.string
                    index +=1

        if data != {}:
            alltemp.append(data)
            index = 0
            data = {}
    global alldata
    alldata = alltemp
    
update()

def autoupdate():
    update()
    print("Updated "+datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

def getdata(country):
    if alldata == []:
        update()
    country = formatinput(country)
    for data in alldata:
        if data['Country'] == country:
            return data
    return []

def getimage(country):
    try:
        return flags[countries.index(country)]
    except:
        return "https://upload.wikimedia.org/wikipedia/commons/thumb/5/55/Question_Mark.svg/1200px-Question_Mark.svg.png"


def fixunknownvalues(data):
    if str(data["Cases"]) == '' or str(data["Cases"]) == 'None':
        data["Cases"] = '0'
    if str(data["Deaths"]) == '' or str(data["Deaths"]) == 'None':
        data["Deaths"] = '0'
    if str(data["Recovered"]) == '' or str(data["Recovered"]) == 'None':
        data["Recovered"] = '0'
    if str(data["NewCases"]) == '' or str(data["NewCases"]) == 'None':
        data["NewCases"] = '0'
    if str(data["NewDeaths"]) == '' or str(data["NewDeaths"]) == 'None':
        data["NewDeaths"] = '0'

    return data

#format result as JSON
def formatresult(gotdata):
    gotdata = fixunknownvalues(gotdata)
    result = {"Country": gotdata['Country'],"Cases": gotdata["Cases"],"CasesToday":gotdata["NewCases"],"Deaths": gotdata["Deaths"],"DeathsToday":gotdata["NewDeaths"],"Recovered": gotdata["Recovered"],"Flag": getimage(gotdata['Country']),"Date": lastupdated[13:]}
    return jsonify(result)

#format country name to fix uppercase and lowercase issues
def formatinput(country):
    if len(country) < 4:
        if country.isupper() == False:
            country = country.upper()
    elif country.isupper():
        country = country.lower().title()
    else :
        country = country.upper().title()
    if "Korea" in country:
        country = "S. Korea"
    return country
  
#scheduler that updates de data every minute
sched = BackgroundScheduler({'apscheduler.timezone': 'UTC'},daemon=True)
sched.add_job(autoupdate,'cron',minute='*')
sched.start()

app = Flask(__name__, static_url_path = "/static")
app.add_url_rule('/<path:filename>', view_func=app.send_static_file)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['JSON_SORT_KEYS'] = False
@app.route("/", methods=['GET'])
def hello():
    f = open("static/index.html", 'r')
    index = f.read()
    f.close()
    return index

@app.route("/<country>", methods=['GET'])
def showdata(country):
    title = formatinput(country)
    data = getdata(title)
    if data == []:
        response = jsonify(
            Error= "Country not Found",
            Country= title
        )
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    else:
        response = formatresult(data)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

if __name__ == "__main__":
    app.run(ssl_context='adhoc')