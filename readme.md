Bienvenidos a MY CRYPTO !
MY CRYPTO  es una aplicacion en la que podras consultar el cambio de 12 tipos de criptomonedas las cuales son: ["EUR","EOS","XRP", "BCH", "ADA", "ETH","XLM","BTN", "USDT","LTC","BNB","TRX","BSV"] , en la pagina de inicio tendras una lista de todos los movimientos realizados;  al pulsar el boton + te enviara a la pagina de compra donde podras registrar un nuevo movimiento  pulsando FROM para escoger la moneda de la cual quieres cambiar , donde Q sera la cantidad que deseas cambiar, TO la moneda que deseas comprar con la cantidad de monedas FROM , siendo asi PU el precio unitario , luego tendras una pagina de estatus donde valor invertido sera la cantidad total de euros invertidos y valor actual sera (total de euros invertidos + saldo de euros invertidos + valor de euros de nuestras cryptos )

PASOS A SEGUIR PARA USAR LA APLICACION:
 
paso 1 : 
# instalacion

para instalar las dependencias ejecutar
```
pip install -r requirements.txt

´´´
paso 2 :

Deberas crearte tu propia apikey en coinmarketcap 

https://coinmarketcap.com/api/

paso 3: 
 Tendras tambien que crear tu entorno virtual (venv)

paso 4: 
deberas crearte tu propia base de datos en sqlite le pondras por nombre basededatos.db en la cual la tabla se llamara movimientos y se podran resgistrar los siguientes datos:
id = integer
data = text NOT NULL
time= text NOT NULL 
from_currency= text NOT NUL 
from_quantity= REAL NOT NUL
to_currency= text NOT NUL 
to_quantity= real NOT NUL 
PU= REAL NOT NOUL 