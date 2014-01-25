package br.com.housepi.activity;

import java.io.IOException;
import java.io.Reader;
import java.io.StringReader;
import org.jdom2.Document;
import org.jdom2.Element;
import org.jdom2.JDOMException;
import org.jdom2.input.SAXBuilder;
import org.jdom2.output.XMLOutputter;
import br.com.housepi.R;
import br.com.housepi.classes.Conexao;
import br.com.housepi.classes.Funcoes;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.content.Context;
import android.annotation.SuppressLint;
import android.support.v4.app.Fragment;
import android.app.ProgressDialog;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.TextView;

public class TemperaturaHumidade extends Fragment implements OnClickListener {
	private Button btnAtualizar;
	private TextView lblTemperatura;
	private TextView lblHumidade;
	private ProgressDialog dialog;
	private String temperatura;
	private String humidade;
	
	public static Fragment newInstance(Context context) {
		TemperaturaHumidade f = new TemperaturaHumidade();
		return f;
	}

	@Override
	public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
		View rootView = inflater.inflate(R.layout.temperatura_humidade, container, false);
		
		btnAtualizar = (Button) rootView.findViewById(R.id.btnAtualizarTempHum);
		btnAtualizar.setOnClickListener(this);
		
		lblTemperatura = (TextView) rootView.findViewById(R.id.lblTemperatura);
		lblHumidade = (TextView) rootView.findViewById(R.id.lblHumidade);
		
		startThreadGetDados();
		
		return rootView;
	}
	
	public void onClick(View view) {
		if (view == btnAtualizar){  
			startThreadGetDados();
		}
	}
	
	@SuppressLint("HandlerLeak")
	private Handler handler = new Handler() {
		public void handleMessage(android.os.Message msg) {
			try {
				synchronized (msg) {
					if (msg.arg1 == 0) {
						Funcoes.msgToastErroComando(getActivity());
					} else {
						if (!temperatura.trim().equals("")) {
							lblTemperatura.setText(temperatura);
						}
						
						if (!humidade.trim().equals("")) {
							lblHumidade.setText(humidade);
						}
					}
				}
			} catch (Exception e) {
				dialog.dismiss();
				startThreadGetDados();
			}
		}
	};

	private void startThreadGetDados() {
		dialog = ProgressDialog.show(this.getActivity(), "Aguarde", "Obtendo dados..."); 
        new Thread() {
            public void run() {
                try{
                	getTemperaturaHumidade();
                } catch (Exception e) {
                    Log.e("tag", e.getMessage());
                }
            }
        }.start();	
	}
	
	public void getTemperaturaHumidade() {
		Document doc = new Document();
		Element root = new Element("Temperatura");
		doc.setRootElement(root);
		
		Conexao.getConexaoAtual().enviarMensagem(new XMLOutputter().outputString(doc));
		
		try {
			String mensagem = "";
			
			mensagem = Conexao.getConexaoAtual().receberRetorno();
			
			if (!mensagem.equals("Erro")){
			
				SAXBuilder builder = new SAXBuilder();
				Reader in = new StringReader(mensagem);
				
				try {
					doc = builder.build(in);
				} catch (JDOMException e) {
					e.printStackTrace();
				}
				
				Element retorno = (Element) doc.getRootElement();
				
				Message msg = new Message();
				msg.arg1 = 1;
				handler.sendMessage(msg);
				
				temperatura = retorno.getChild("Dados").getAttribute("Temperatura").getValue() + " ºC";
				humidade = retorno.getChild("Dados").getAttribute("Humidade").getValue() + " %";
				dialog.dismiss();
			} else {
				Message msg = new Message();
				msg.arg1 = 0;
				handler.sendMessage(msg);
				
				dialog.dismiss();
			}
		} catch (IOException e) {
			e.printStackTrace();
			dialog.dismiss();
		}
	}
}
