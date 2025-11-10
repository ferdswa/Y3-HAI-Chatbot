import numpy
import scipy
import pickle
from urllib import request

doc_urls = {" Russia " : " http :// www . gutenberg . org / cache / epub /13437/ pg13437 . txt " ,
             " France " : " http :// www . gutenberg . org / cache / epub /10577/ pg10577 . txt " ,
 " England " : " http :// www . gutenberg . org / cache / epub /10135/ pg10135 . txt " ,
 " USA " : " http :// www . gutenberg . org / cache / epub /10947/ pg10947 . txt " ,
 " Spain " : " http :// www . gutenberg . org / cache / epub /9987/ pg9987 . txt " ,
 " Scandinavia " : " http :// www . gutenberg . org / cache / epub /5336/ pg5336 . txt " ,
 " Iceland " : " http :// www . gutenberg . org / cache / epub /5603/ pg5603 . txt"}