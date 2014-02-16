package br.com.housepi.activity;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import br.com.housepi.R;
import br.com.housepi.classes.Agendamento;
import br.com.housepi.classes.Funcoes;
import android.os.Bundle;
import android.annotation.SuppressLint;
import android.content.Context;
import android.content.Intent;
import android.support.v4.app.Fragment;
import android.text.Editable;
import android.text.TextWatcher;
import android.view.ContextMenu;
import android.view.ContextMenu.ContextMenuInfo;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.SimpleAdapter;
import android.widget.Toast;

@SuppressLint({ "InlinedApi"})
public class ControleAgendamento extends Fragment implements OnClickListener {
	private ListView listView;
	private static final ArrayList<HashMap<String,String>> listaVisualizacao = new ArrayList<HashMap<String,String>>(); 
	private List<Agendamento> agendamentos = new ArrayList<Agendamento>();
	private String[] menuItems = new String[] {"Remover"};
	private SimpleAdapter adapter;
	private Button btnNovo;
	private EditText edtPesquisar;
	
	public static Fragment newInstance(Context context) {
		ControleAgendamento f = new ControleAgendamento();
		return f;
	}

	@Override
	public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
		View rootView = inflater.inflate(R.layout.controle_agendamento, container, false);

		edtPesquisar = (EditText) rootView.findViewById(R.id.edtPesquisar);
		
		btnNovo = (Button) rootView.findViewById(R.id.btnNovo);
		btnNovo.setOnClickListener(this);
		
		listView = (ListView) rootView.findViewById(R.id.listAgendamentos);

		adapter = new SimpleAdapter(
        		this.getActivity(),
        		listaVisualizacao,
        		R.layout.linha_list_view,
        		new String[] {"Nome", "Ligar", "Desligar", "Dias", "Equipamento"},
        		new int[] {R.id.lvNome, R.id.lvLigar, R.id.lvDesligar, R.id.lvDias, R.id.lvEquipamento}
        		);
		
		listView.setAdapter(adapter);
		registerForContextMenu(listView);
        
        edtPesquisar.addTextChangedListener(new TextWatcher() {
        	 
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
	
	private void carregarAgendamentos(Boolean getServidor) {
		if (getServidor) {
			agendamentos = Agendamento.getAgendamentos();
		}
			
		listaVisualizacao.clear();
		
		for (Agendamento agendamento : agendamentos) {
			String dias = agendamento.getDiasDaSemana();
			
			dias = dias.replace("0", "Dom");
			dias = dias.replace("1", "Seg");
			dias = dias.replace("2", "Ter");
			dias = dias.replace("3", "Qua");
			dias = dias.replace("4", "Qui");
			dias = dias.replace("5", "Sex");
			dias = dias.replace("6", "Sab");
			
			if (dias.trim().equals("")) {
				dias = "Nenhum";
			}
			
			addListaVisualizacao(agendamento.getNome(), Funcoes.formatarDataHoraLocal(agendamento.getDataHoraInicial()), Funcoes.formatarDataHoraLocal(agendamento.getDataHoraFinal()), dias, "'" + agendamento.getNomeEquipamentos() + "'");
		}
		adapter.notifyDataSetChanged();
	}
	
	private void addListaVisualizacao(String nome, String ligar, String desligar, String dias, String equipamento) {
    	HashMap<String,String> temp = new HashMap<String,String>();
    	temp.put("Nome", nome + "  ");
    	temp.put("Ligar", "Ligar: " + ligar + "  ");
    	temp.put("Desligar", "Desligar: " + desligar + "  ");
    	temp.put("Dias", "Repetir: " + dias + "  ");
    	temp.put("Equipamento", "Equipamento: " + equipamento + "  ");
    	listaVisualizacao.add(temp);
    }

		
	@Override
	public void onCreateContextMenu(ContextMenu menu, View v,
	    ContextMenuInfo menuInfo) {
	  if (v.getId()==R.id.listAgendamentos) {
	    
		  menu.setHeaderTitle("O que deseja fazer?");
	    
	    for (int i = 0; i<menuItems.length; i++) {
	      menu.add(Menu.NONE, i, i, menuItems[i]);
	    }
	  }
	}
	
	@Override
	public boolean onContextItemSelected(MenuItem item) {
	  AdapterView.AdapterContextMenuInfo info = (AdapterView.AdapterContextMenuInfo)item.getMenuInfo();
	  
	  if (agendamentos.get(info.position).removerAgendamento()) {
		  Toast.makeText(this.getActivity(), "Agendamento removido com sucesso!", Toast.LENGTH_LONG).show();
		  agendamentos.remove(info.position);
		  listaVisualizacao.remove(info.position);
		  carregarAgendamentos(false);
	  } else {
		  Toast.makeText(this.getActivity(), "Não foi possível remover o agendamento.", Toast.LENGTH_LONG).show();
	  }
				  
	  return true;
	}

	@Override
	public void onClick(View v) {
		if (v == btnNovo) {
			startActivity(new Intent(this.getActivity(), CadastroAgendamento.class));
		}
	}
	
	@Override
	public void onResume() {
		super.onResume();
		
		edtPesquisar.getText().clear();
		carregarAgendamentos(true);
	}
}
