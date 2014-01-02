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
import android.os.Bundle;
import android.content.Context;
import android.annotation.SuppressLint;
import android.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.TextView;

@SuppressLint("NewApi")
public class TemperaturaHumidade extends Fragment implements OnClickListener {
	private Button btnAtualizar;
	private TextView lblTemperatura;
	private TextView lblHumidade;
	
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
		
		//getTemperaturaHumidade();
		
		return rootView;
	}
	
	public void onClick(View view) {
		if (view == btnAtualizar){  
			getTemperaturaHumidade();
		}
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
				
				lblTemperatura.setText("Temperatura: " + retorno.getChild("Dados").getAttribute("Temperatura").getValue() + " ºC");
				lblHumidade.setText("Humidade: " + retorno.getChild("Dados").getAttribute("Humidade").getValue() + " %");
			} else {
				lblTemperatura.setText("Erro ao obter Temperatura");
				lblHumidade.setText("Erro ao obter Humidade");
			}
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

}
