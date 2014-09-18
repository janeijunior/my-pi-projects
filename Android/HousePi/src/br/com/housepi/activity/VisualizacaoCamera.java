package br.com.housepi.activity;

import java.io.IOException;
import java.io.Reader;
import java.io.StringReader;
import java.net.URI;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import org.apache.http.HttpResponse;
import org.apache.http.auth.AuthScope;
import org.apache.http.auth.UsernamePasswordCredentials;
import org.apache.http.client.CredentialsProvider;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.BasicCredentialsProvider;
import org.apache.http.impl.client.DefaultHttpClient;
import org.jdom2.Document;
import org.jdom2.Element;
import org.jdom2.JDOMException;
import org.jdom2.input.SAXBuilder;
import org.jdom2.output.XMLOutputter;

import br.com.housepi.activity.Login;
import android.content.Context;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.AdapterView.OnItemSelectedListener;
import android.widget.ArrayAdapter;
import android.widget.LinearLayout;
import android.widget.Spinner;
import br.com.housepi.R;
import br.com.housepi.bibliotecas.MjpegInputStream;
import br.com.housepi.bibliotecas.MjpegView;
import br.com.housepi.classes.Conexao;

public class VisualizacaoCamera extends Fragment implements OnItemSelectedListener {

	private MjpegView mv;
	private Spinner spinner;
	private LinearLayout llCamera;
	private List<String> cameras = new ArrayList<String>();
	
	public static Fragment newInstance(Context context) {
		VisualizacaoCamera f = new VisualizacaoCamera();
		return f;
	}

	@Override
	public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
		View rootView = inflater.inflate(R.layout.visualizacao_camera, container, false);
	
		llCamera = (LinearLayout) rootView.findViewById(R.id.llCamera);
		
		spinner = (Spinner) rootView.findViewById(R.id.spCamera); 
        spinner.setOnItemSelectedListener(this);
 
        carregarCamera();
 
        ArrayAdapter<String> dataAdapter = new ArrayAdapter<String>(rootView.getContext(), android.R.layout.simple_spinner_item, cameras);
        dataAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        spinner.setAdapter(dataAdapter);
        
		return rootView;
	}

	private void conectar(String url) {
		try {
			HttpResponse res = null;
			DefaultHttpClient httpclient = new DefaultHttpClient();
			
			CredentialsProvider credProvider = new BasicCredentialsProvider();
		    credProvider.setCredentials(new AuthScope(AuthScope.ANY_HOST, AuthScope.ANY_PORT), new UsernamePasswordCredentials(Login.USUARIO, Login.SENHA));
		    
		    httpclient.setCredentialsProvider(credProvider);
			
			res = httpclient.execute(new HttpGet(URI.create(url)));

			mv.setSource(new MjpegInputStream(res.getEntity().getContent()));
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
		
	@Override
	public void onPause() {
		mv.destroyDrawingCache();
		mv.stopPlayback();
		super.onPause();
	}

	@Override
	public void onItemSelected(AdapterView<?> arg0, View arg1, int arg2, long arg3) {
		if (mv != null) {
			mv.destroyDrawingCache();
			mv.stopPlayback();
			llCamera.removeView(mv);
		}
		
		mv = new MjpegView(this.getActivity());
		llCamera.addView(mv);
		mv.setDisplayMode(MjpegView.SIZE_BEST_FIT);
		mv.showFps(false);
		
		String url = "http://" + Login.IP_SERVIDOR + ":" + getPortaCamera(spinner.getItemAtPosition(spinner.getSelectedItemPosition()).toString()) + "/?action=stream";
		conectar(url);
	}

	@Override
	public void onNothingSelected(AdapterView<?> arg0) {
		
	}
	
	public String getPortaCamera(String nome) {
		Document doc = new Document();
		Element root = new Element("PortaCamera");
		root.addContent(new Element("Nome").setText(nome));
		doc.setRootElement(root);
		
		Conexao.getConexaoAtual().enviarMensagem(new XMLOutputter().outputString(doc));
		
		return Conexao.receberRetornoStatic();
	}

	private void carregarCamera() {
		Document doc = new Document();
		String mensagem = "";
		
		Element root = new Element("EnviarCamera");
		doc.setRootElement(root);

		Conexao.getConexaoAtual().enviarMensagem(new XMLOutputter().outputString(doc));

		mensagem = Conexao.getConexaoAtual().receberRetorno();
					
		SAXBuilder builder = new SAXBuilder();
		Reader in = new StringReader(mensagem);

		try {
			doc = builder.build(in);
		} catch (JDOMException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
		
		Element retorno = (Element) doc.getRootElement();
		
		cameras.clear();
		
		if (retorno.getName().equals("EnviarCamera")) {
			@SuppressWarnings("rawtypes")
			List elements = retorno.getChildren();
			@SuppressWarnings("rawtypes")
			Iterator j = elements.iterator();
	
			while (j.hasNext()) {
				Element element = (Element) j.next();
				cameras.add(element.getAttribute("Nome").getValue());
			}
		}
	}
}
