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
import android.annotation.SuppressLint;
import android.app.Fragment;
import android.view.ContextMenu;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.ViewGroup;
import android.view.ContextMenu.ContextMenuInfo;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ImageButton;
import android.widget.ListView;
import android.widget.SeekBar;
import android.widget.TextView;
import android.widget.SeekBar.OnSeekBarChangeListener;

@SuppressLint("NewApi")
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
	private List<String> musicas = new LinkedList<String>();
	private String[] menuItems = new String[] {"Executar"};

	public static Fragment newInstance(Context context) {
		ControleSomAmbiente f = new ControleSomAmbiente();
		return f;
	}

	@Override
	public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
		View rootView = inflater.inflate(R.layout.controle_som_ambiente,
				container, false);

		lblVolume = (TextView) rootView.findViewById(R.id.lblVolume);
		
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
		
		listView = (ListView) rootView.findViewById(R.id.listMusica);

		adapter = new ArrayAdapter<String>(this.getActivity(), android.R.layout.simple_list_item_1, android.R.id.text1, musicas);

		listView.setAdapter(adapter);
		registerForContextMenu(listView);
		
		getMusicas();

		return rootView;
	}
	
	@Override
	public void onCreateContextMenu(ContextMenu menu, View v,
	    ContextMenuInfo menuInfo) {
	  if (v.getId( )== R.id.listMusica) {
	    menu.setHeaderTitle("O que deseja fazer?");
	    
	    for (int i = 0; i < menuItems.length; i++) {
	      menu.add(Menu.NONE, i, i, menuItems[i]);
	    }
	  }
	}
	
	@Override
	public boolean onContextItemSelected(MenuItem item) {
		AdapterView.AdapterContextMenuInfo info = (AdapterView.AdapterContextMenuInfo)item.getMenuInfo();
		//int menuItemIndex = item.getItemId();
		//String menuItemName = menuItems[menuItemIndex];
	  
		//String musica = musicas.get(info.position).toString();	  
		
		String atual = enviarComandoResposta("EnviarNomeArquivo", "0");
		atual = atual.substring(1, atual.length() -1);
		Integer indiceAtual = musicas.indexOf(atual);		
		
		Integer valor = info.position - indiceAtual;
		
		if (valor != 0) {
			enviarComando("AnteriorProxima", String.valueOf(valor));
		}
			
		return true;
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
			
			@SuppressWarnings("rawtypes")
			List elements = retorno.getChildren();
			@SuppressWarnings("rawtypes")
			Iterator j = elements.iterator();
			
			while (j.hasNext()) {
				Element element = (Element) j.next();
				musicas.add(element.getAttribute("Nome").getValue());
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
	
	private String enviarComandoResposta(String comando, String valor) {
		try {
			Document doc = new Document();
			Element root = new Element("ControlarSomAmbiente");
				
			root.addContent(new Element("Comando").setText(comando));
			root.addContent(new Element("Valor").setText(valor));
			
			doc.setRootElement(root);
	
			Conexao.getConexaoAtual().enviarMensagem(new XMLOutputter().outputString(doc));
			
			String mensagem = "";
	
			mensagem = Conexao.getConexaoAtual().receberRetorno();
	
			return mensagem;
		} catch (Exception e) {
			e.printStackTrace();
			return "";
		}		
	}
}
