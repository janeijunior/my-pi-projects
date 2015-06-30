**Bem vindo!**

* Os  fontes do aplicativo servidor encontram-se na pasta Servidor, o mesmo foi desenvolvido em Python utilizando a WebIDE da Adafruit.
 
* Já os do aplicativo mobile encontram-se na pasta Android e foi desenvolvido em Java utilizando o Eclipse Juno.
 
* Na pasta documentos encontram-se alguns arquivos que podem ser úteis.
 
* Na pasta Instaladores será possível encontrar a versão compilada dos aplicativos.
 
* A instalação das dependências (no Raspberry Pi) pode ser feita de maneira automática seguindo os passos do vídeo: https://www.youtube.com/watch?v=r7ZKW1A3y1I
 
* Após executar a instalação indicada no vídeo acima sugere-se instalar a IDE: https://learn.adafruit.com/webide/installation e clonar este repositório. Para iniciar o aplicativo automaticamanete pelos fontes e não pelos arquivos compilados gerados pela instalação automatica basta modificar o local da inicialização que esta no final do arquivo: /etc/init.d/rc.local

* Pode ser necessário executar novamente o script de criação do banco (ScriptBanco.sql) pois aqui pode estar mais atualizado, verifique também o nome do usuário do banco no arquivo Config.ini o mesmo deve ser "HousePi".

* Se for utilizar o Eclipse para o projeto Android importe o mesmo juntamente com a appcompat v7 support library, pode ser necessário atualizar sua referencia no projeto principal.

* O Apk também encontra-se na Google Play: https://play.google.com/store/apps/details?id=br.com.housepi 


**Imagens:**

![Screenshot_2014-05-17-14-07-11.png](https://bitbucket.org/repo/KbG8KA/images/2324044091-Screenshot_2014-05-17-14-07-11.png)![20140509_003926_Android.jpg](https://bitbucket.org/repo/KbG8KA/images/2019319887-20140509_003926_Android.jpg)