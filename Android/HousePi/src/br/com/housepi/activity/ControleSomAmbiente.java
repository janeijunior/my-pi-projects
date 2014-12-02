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
import br.com.housepi.R;
import br.com.housepi.classes.Conexao;
import br.com.housepi.classes.Funcoes;
import android.os.Bundle;
import android.content.Context;
import android.support.v4.app.Fragment;
import android.text.Editable;
import android.text.TextWatcher;
import android.view.LayoutInflater;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.AdapterView.OnItemClickListener;
import android.widget.ArrayAdapter;
import android.widget.EditText;
import android.widget.ImageButton;
import android.widget.ListView;
import android.widget.RadioButton;
import android.widget.SeekBar;
import android.widget.TextView;
import android.widget.SeekBar.OnSeekBarChangeListener;

public class ControleSomAmbiente extends Fragment implements OnClickListener, OnSeekBarChangeListener {
	private ListView listView;
	private TextView lblVolume;
	private ImageButton btnAnterior;
	private ImageButton btnPlay;
	private ImageButton btnPause;
	private ImageButton btnStop;
	private ImageButton btnProxima;	
	private SeekBar sbVolume;
	private ArrayAdapter<String> adapter;
	private EditText edtPesquisaMusica;
	private List<String> musicas = new LinkedList<String>();
	private RadioButton rbHDMI;
	private RadioButton rbP2;
	
	public static Fragment newInstance(Context context) {
		ControleSomAmbiente f = new ControleSomAmbiente();
		return f;
	}

	@Override
	public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
		View rootView = inflater.inflate(R.layout.controle_som_ambiente,
				container, false);

		lblVolume = (TextView) rootView.findViewById(R.id.lblVolume);
		
		edtPesquisaMusica = (EditText) rootView.findViewById(R.id.edtPesquisaMusica);
		
		btnAnterior = (ImageButton) rootView.findViewById(R.id.btnAnterior);
		btnAnterior.setOnClickListener(this);
		
		btnProxima = (ImageButton) rootView.findViewById(R.id.btnProxima);
		btnProxima.setOnClickListener(this);
		
		btnPlay = (ImageButton) rootView.findViewById(R.id.btnPlay);
		btnPlay.setOnClickListener(this);
		
		btnPause = (ImageButton) rootView.findViewById(R.id.btnPause);
		btnPause.setOnClickListener(this);
		
		btnStop = (ImageButton) rootView.findViewById(R.id.btnStop);
		btnStop.setOnClickListener(this);
		
		sbVolume = (SeekBar) rootView.findViewById(R.id.sbVolume);
		sbVolume.setOnSeekBarChangeListener(this);
		String vol = Funcoes.carregarDadosComponente("sbVolume", "60", this.getActivity());
		sbVolume.setProgress(Integer.parseInt(vol));
		sbVolume.refreshDrawableState();
		
		rbHDMI = (RadioButton) rootView.findViewById(R.id.rbHDMI);
		rbP2 = (RadioButton) rootView.findViewById(R.id.rbP2);

		String tipoAudio = Funcoes.carregarDadosComponente("TipoAudio", "2", this.getActivity());
		
		rbHDMI.setChecked(tipoAudio.equals("2"));
		rbP2.setChecked(tipoAudio.equals("1"));
		
		enviarComando("TipoAudio", tipoAudio);
		
		rbHDMI.setOnClickListener(this);
		rbP2.setOnClickListener(this);
		
		listView = (ListView) rootView.findViewById(R.id.listMusica);
				
		adapter = new ArrayAdapter<String>(this.getActivity(), R.layout.linha_list_view_musica, R.id.listNomeMusica, musicas);

		listView.setAdapter(adapter);
		registerForContextMenu(listView);
		
		getMusicas();
		
		listView.setOnItemClickListener(new OnItemClickListener() {
	        public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
	        	
	        	String nome = listView.getItemAtPosition(position).toString();
	        		
	        	enviarComando("ReproduzirPorNome", nome);
	        }
	    });
		
		edtPesquisaMusica.addTextChangedListener(new TextWatcher() {
        	 
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
			Element root = new Element("EnviarListaMusica");
			doc.setRootElement(root);
	
			Conexao.getConexaoAtual().enviarMensagem(new XMLOutputter().outputString(doc));
	
			String mensagem = "";
			musicas.clear();
	
			mensagem = Conexao.getConexaoAtual().receberRetorno();
	
			SAXBuilder builder = new SAXBuilder();
			Reader in = new StringReader(mensagem);
	
			try {
				doc = builder.build(in);
			} catch (JDOMException e) {
				e.printStackTrace();
			}
	
			Element retorno = (Element) doc.getRootElement();
			
			if (!retorno.getName().equals("EnviarListaMusica")) {
				Funcoes.msgToastErroComando(this.getActivity());
				return;
			}
			
			@SuppressWarnings("rawtypes")
			List elements = retorno.getChildren();
			@SuppressWarnings("rawtypes")
			Iterator j = elements.iterator();
			
			while (j.hasNext()) {
				Element element = (Element) j.next();
				String musica = element.getAttribute("Nome").getValue();
				musicas.add(musica.substring(0, musica.length() - 4));
			}
			
			adapter.notifyDataSetChanged();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	@Override
	public void onClick(View v) {
		if (v == btnPlay) {
			enviarComando("Play", "0");
			
			try {
				Thread.sleep(200);
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
			
			enviarComando("Volume", String.valueOf(sbVolume.getProgress()));
		} else if (v == btnPause) {
			enviarComando("Pause", "0");
		} else if (v == btnStop) {
			enviarComando("Stop", "0");
		} else if (v == btnAnterior) {
			enviarComando("AnteriorProxima", "-1");
		} else if (v == btnProxima) {
			enviarComando("AnteriorProxima", "1");
		} else if (v == rbHDMI) {
			enviarComando("TipoAudio", "2");
			Funcoes.salvarDadosComponente("TipoAudio", "2", this.getActivity());
		} else if (v == rbP2) {
			enviarComando("TipoAudio", "1");
			Funcoes.salvarDadosComponente("TipoAudio", "1", this.getActivity());
		}
	}
	
	@Override
    public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
		lblVolume.setText(progress + "");
    }

	@Override
	public void onStartTrackingTouch(SeekBar seekBar) {
		
	}

	@Override
	public void onStopTrackingTouch(SeekBar seekBar) {
		Integer vol = seekBar.getProgress();
		
		Funcoes.salvarDadosComponente("sbVolume", vol.toString(), this.getActivity());
		
		enviarComando("Volume", vol.toString());
	}
	
	private void enviarComando(String comando, String valor) {
		Document doc = new Document();
		Element root = new Element("ControlarSomAmbiente");
			
		root.addContent(new Element("Comando").setText(comando));
		root.addContent(new Element("Valor").setText(valor));
		
		doc.setRootElement(root);

		Conexao.getConexaoAtual().enviarMensagem(new XMLOutputter().outputString(doc));
	}
}
