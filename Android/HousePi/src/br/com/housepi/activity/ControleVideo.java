package br.com.housepi.activity;

import java.io.Reader;
import java.io.StringReader;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.List;

import org.jdom2.Document;
import org.jdom2.Element;
import org.jdom2.JDOMException;
import org.jdom2.input.SAXBuilder;
import org.jdom2.output.XMLOutputter;

import br.com.housepi.*;
import br.com.housepi.classes.Conexao;
import br.com.housepi.classes.Funcoes;
import android.support.v4.app.Fragment;
import android.text.Editable;
import android.text.TextWatcher;
import android.content.Context;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.view.View.OnClickListener;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.EditText;
import android.widget.ImageButton;
import android.widget.ListView;
import android.widget.AdapterView.OnItemClickListener;

public class ControleVideo extends Fragment implements OnClickListener {
	
	private ListView listView;
	private ImageButton btnRetroceder;
	private ImageButton btnAvancar;
	private ImageButton btnPause;
	private ImageButton btnStop;
	private ArrayAdapter<String> adapter;
	private EditText edtPesquisaVideo;
	private List<String> videos = new LinkedList<String>();
	
	public static Fragment newInstance(Context context) {
		ControleVideo f = new ControleVideo();
		return f;
	}

	@Override
	public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
		View rootView = inflater.inflate(R.layout.controle_video,
				container, false);
		
		edtPesquisaVideo = (EditText) rootView.findViewById(R.id.edPesquisaVideo);
		
		btnRetroceder = (ImageButton) rootView.findViewById(R.id.btRetrocederVideo);
		btnRetroceder.setOnClickListener(this);
		
		btnAvancar = (ImageButton) rootView.findViewById(R.id.btAvancarVideo);
		btnAvancar.setOnClickListener(this);
		
		btnPause = (ImageButton) rootView.findViewById(R.id.btPauseVideo);
		btnPause.setOnClickListener(this);
		
		btnStop = (ImageButton) rootView.findViewById(R.id.btStopVideo);
		btnStop.setOnClickListener(this);
		
		listView = (ListView) rootView.findViewById(R.id.lvVideo);
				
		adapter = new ArrayAdapter<String>(this.getActivity(), R.layout.linha_list_view_musica, R.id.listNomeMusica, videos);

		listView.setAdapter(adapter);
		registerForContextMenu(listView);
		
		getMusicas();
		
		listView.setOnItemClickListener(new OnItemClickListener() {
	        public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
	        	
	        	String nome = listView.getItemAtPosition(position).toString();
	        		
	        	enviarComando("ReproduzirPorNome", nome);
	        }
	    });
		
		edtPesquisaVideo.addTextChangedListener(new TextWatcher() {
        	 
			public void afterTextChanged(Editable s) {
       	  
       	  	}
       	 
			public void beforeTextChanged(CharSequence s, int start, int count, int after) {
       	
			}
       	 
       	  	public void onTextChanged(CharSequence s, int start, int before, int count) {
       	  		adapter.getFilter().filter(s.toString());
       	  	}
        });

		return rootView;
	}

	private void getMusicas() {
		try {
			Document doc = new Document();
			Element root = new Element("EnviarListaVideo");
			doc.setRootElement(root);
	
			Conexao.getConexaoAtual().enviarMensagem(new XMLOutputter().outputString(doc));
	
			String mensagem = "";
			videos.clear();
	
			mensagem = Conexao.getConexaoAtual().receberRetorno();
	
			SAXBuilder builder = new SAXBuilder();
			Reader in = new StringReader(mensagem);
	
			try {
				doc = builder.build(in);
			} catch (JDOMException e) {
				e.printStackTrace();
			}
	
			Element retorno = (Element) doc.getRootElement();
			
			if (!retorno.getName().equals("EnviarListaVideo")) {
				Funcoes.msgToastErroComando(this.getActivity());
				return;
			}
			
			@SuppressWarnings("rawtypes")
			List elements = retorno.getChildren();
			@SuppressWarnings("rawtypes")
			Iterator j = elements.iterator();
			
			while (j.hasNext()) {
				Element element = (Element) j.next();
				String video = element.getAttribute("Nome").getValue();
				//videos.add(video.substring(0, video.length() - 4));
				videos.add(video);
			}
			
			adapter.notifyDataSetChanged();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	@Override
	public void onClick(View v) {
		if (v == btnPause) {
			enviarComando("Pause", "0");
		} else if (v == btnStop) {
			enviarComando("Stop", "0");
		} else if (v == btnAvancar) {
			enviarComando("Avancar", "0");
		} else if (v == btnRetroceder) {
			enviarComando("Retroceder", "0");
		}
	}
	
	private void enviarComando(String comando, String valor) {
		Document doc = new Document();
		Element root = new Element("ControlarVideo");
			
		root.addContent(new Element("Comando").setText(comando));
		root.addContent(new Element("Valor").setText(valor));
		
		doc.setRootElement(root);

		Conexao.getConexaoAtual().enviarMensagem(new XMLOutputter().outputString(doc));
	}
}
