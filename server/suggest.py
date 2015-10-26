# -*- coding: utf-8 -*-

import scipy.sparse, scipy.io
import numpy as np
import pickle

def save_sparse_csr(filename,array):
    np.savez_compressed(filename,data = array.data ,indices=array.indices,
             indptr =array.indptr, shape=array.shape )

def load_sparse_csr(filename):
    loader = np.load(filename)
    return scipy.sparse.csr_matrix((  loader['data'], loader['indices'], loader['indptr']),
                         shape = loader['shape'])

maxsmallid = 1000000

class Predictor():
    
    def __init__(self, userinfo='userinfo.npz', countryinfo='r_country2.npz',
                    cityinfo='r_city.npz', uniinfo='r_uni.npz'):
        print 'started'
        #data = np.load(userinfo)
        #self.countryids = data['countryids'][:maxsmallid]
        #self.cityids = data['cityids'][:maxsmallid]
        #self.uniids = data['uniids'][:maxsmallid]
        #del(data)
        #print 'userinfo loaded'
        self.countryinfo = load_sparse_csr(countryinfo)
        print 'countryinfo loaded'
        self.cityinfo = load_sparse_csr(cityinfo)
        print 'cityinfo loaded'
        self.uniinfo = load_sparse_csr(uniinfo)
        print 'uniinfo loaded'
        self.id2c = np.array(pickle.load(open('id2c.p', 'rb')))
        self.id2ci = np.array(pickle.load(open('id2ci.p', 'rb')))
        
        
    def get_predictions(self, uid, topn=3):
        if uid > maxsmallid or uid < 1:
            return None
        
        data_co = np.array(self.countryinfo[uid].todense())[0]
        argsorted_co = data_co.argsort()[:-topn-1:-1]
        
        data_city = np.array(self.cityinfo[uid].todense())[0]
        argsorted_city = data_city.argsort()[:-topn-1:-1]
        
        data_uni = np.array(self.uniinfo[uid].todense())[0]
        argsorted_uni = data_uni.argsort()[:-topn-1:-1]
        
        return {'Country': [(x,self.id2c[y+1]) for (x,y) in zip(data_co[argsorted_co], argsorted_co)],
                'City': [(x,self.id2ci[y+1]) for (x,y) in zip(data_city[argsorted_city], argsorted_city)],
                'University': zip(data_uni[argsorted_uni], argsorted_uni + 1)}

        
p = Predictor()

def suggest(uid=1):
    #return {'Country': zip([0.7, 0.2, 0.1], [1,2,3]),
    #'City': zip([0.7, 0.2, 0.1], [1,2,3])}
    return p.get_predictions(uid)