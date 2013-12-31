package br.com.housepi.activity;

import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.HashMap;
import java.util.List;

import br.com.housepi.R;
import br.com.housepi.bibliotecas.DateTimePickerDialog;
import br.com.housepi.bibliotecas.Helper;
import br.com.housepi.classes.Agendamento;
import br.com.housepi.classes.Alarme;
import br.com.housepi.classes.Funcoes;
import br.com.housepi.classes.Rele;
import android.os.Bundle;
import android.annotation.SuppressLint;
import android.app.AlertDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.support.v4.app.Fragment;
import android.util.Log;
import android.view.ContextMenu;
import android.view.ContextMenu.ContextMenuInfo;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.SimpleAdapter;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

@SuppressLint({ "InlinedApi", "NewApi" })
public class ControleAgendamento extends Fragment implements OnClickListener {
	private Spinner spinner;
	private Button btnDefinirInicial;
	private Button btnDefinirFinal;
	private Button btnAdicionar;
	private TextView lblDataHoraInicial;
	private TextView lblDataHoraFinal;
	private EditText edtNome;
	private Integer identificador;
	private ListView listView;
	private Date dataHoraInicial;
	private Date dataHoraFinal;
	private static final ArrayList<HashMap<String,String>> listaVisualizacao = new ArrayList<HashMap<String,String>>(); 
	private List<Agendamento> agendamentos = new ArrayList<Agendamento>();
	private String[] menuItems = new String[] {"Remover"};
	private SimpleAdapter adapter;
	
	public static Fragment newInstance(Context context) {
		ControleAgendamento f = new ControleAgendamento();
		return f;
	}

	@Override
	public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
		View rootView = inflater.inflate(R.layout.controle_agendamento, container, false);
		
		btnDefinirInicial = (Button) rootView.findViewById(R.id.btnDataHoraInicial);
		btnDefinirInicial.setOnClickListener(this);

		btnDefinirFinal = (Button) rootView.findViewById(R.id.btnDataHoraFinal);
		btnDefinirFinal.setOnClickListener(this);

		btnAdicionar = (Button) rootView.findViewById(R.id.btnAdicionar);
		btnAdicionar.setOnClickListener(this);

		lblDataHoraInicial = (TextView) rootView.findViewById(R.id.lblDataHoraInicial);
		lblDataHoraFinal = (TextView) rootView.findViewById(R.id.lblDataHoraFinal);

		edtNome = (EditText) rootView.findViewById(R.id.edtNomeAgendamento);
		
		listView = (ListView) rootView.findViewById(R.id.listAgendamentos);

		addItensSpinner(rootView);

		adapter = new SimpleAdapter(
        		this.getActivity(),
        		listaVisualizacao,
        		R.layout.linha_list_view,
        		new String[] {"Nome", "Ligar", "Desligar", "Equipamento"},
        		new int[] {R.id.lvNome, R.id.lvLigar, R.id.lvDesligar, R.id.lvEquipamento}
        		);
		
		listView.setAdapter(adapter);
		registerForContextMenu(listView);
        
        carregarAgendamentos(true);
        
		return rootView;
	}
	
	private void carregarAgendamentos(Boolean getServidor) {
		
		if (getServidor) {
			agendamentos = Agendamento.getAgendamentos();
		}
			
		listaVisualizacao.clear();
		
		for (Agendamento agendamento : agendamentos) {
			
			if (agendamento.getAlarme() != null) {
				addListaVisualizacao(agendamento.getNome(), Funcoes.formatarDataHoraLocal(agendamento.getDataHoraInicial()), Funcoes.formatarDataHoraLocal(agendamento.getDataHoraFinal()), "Alarme");
			} else {
				addListaVisualizacao(agendamento.getNome(), Funcoes.formatarDataHoraLocal(agendamento.getDataHoraInicial()), Funcoes.formatarDataHoraLocal(agendamento.getDataHoraFinal()), agendamento.getRele().getNome());
			}
		}
		
		adapter.notifyDataSetChanged();
	}
	
	private void addListaVisualizacao(String nome, String ligar, String desligar, String equipamento) {
    	HashMap<String,String> temp = new HashMap<String,String>();
    	temp.put("Nome", nome);
    	temp.put("Ligar", "Ligar: " + ligar);
    	temp.put("Desligar", "Desligar: " + desligar);
    	temp.put("Equipamento", "Equipamento: " + equipamento);
    	listaVisualizacao.add(temp);
    }

	public void onClick(View view) {
		if (view == btnDefinirInicial) {
			identificador = 1;
			showDateTimePicker();
		} else if (view == btnDefinirFinal) {
			identificador = 2;
			showDateTimePicker();
		} else if (view == btnAdicionar) {
			if (dataHoraInicial == null) {
				Funcoes.exibirDialogoInformacao("Atenção", "Informe a data e a hora que deseja ligar o equipamento.", this.getActivity());
			} else if (dataHoraFinal == null) {
				Funcoes.exibirDialogoInformacao("Atenção", "Informe a data e a hora que deseja desligar o equipamento.", this.getActivity());
			} else if (dataHoraInicial.after(dataHoraFinal)) {
				Funcoes.exibirDialogoInformacao("Atenção", "A data/hora de desligamento deve ser maior que a data/hora de acionamento.", this.getActivity());
			} else if (edtNome.getText().toString().trim().equals("")) {
				Funcoes.exibirDialogoInformacao("Atenção", "Informe um nome antes de continuar.", this.getActivity());
			} else {
				Agendamento agendamento;
				
				if (spinner.getSelectedItemPosition() == 0) {
					agendamento = new Agendamento(edtNome.getText().toString().trim(), dataHoraInicial, dataHoraFinal, new Alarme());
				} else {
					agendamento = new Agendamento(edtNome.getText().toString().trim(), dataHoraInicial, dataHoraFinal, new Rele(spinner.getSelectedItemPosition() - 1));
				}
				
				if (agendamento.gravarAgendamento()) {
					Toast.makeText(this.getActivity(), "Agendamento inserido com sucesso!", Toast.LENGTH_LONG).show();
				
					carregarAgendamentos(true);
					
					dataHoraInicial = null;
					dataHoraFinal = null;
					
					edtNome.getText().clear();
					lblDataHoraInicial.setText("Data e Hora");
					lblDataHoraFinal.setText("Data e Hora");
					listView.setSelection(0);
				} else {
					Toast.makeText(this.getActivity(), "Não foi possível inserir o agendamento.", Toast.LENGTH_LONG).show();
				}
			}
		}
	}

	public void addItensSpinner(View rootView) {

		spinner = (Spinner) rootView.findViewById(R.id.spinnerAlarmeRele);

		List<Rele> listaReles = new ArrayList<Rele>();

		for (int i = 0; i < 10; i++) {
			listaReles.add(new Rele(i, null));
		}

		Rele.getConfiguracaoStatus(listaReles);

		List<String> lista = new ArrayList<String>();
		lista.add("Alarme");

		for (Rele rele : listaReles) {
			lista.add(rele.getNome());
		}

		ArrayAdapter<String> dataAdapter = new ArrayAdapter<String>(this.getActivity(), android.R.layout.simple_spinner_item, lista);
		dataAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
		spinner.setAdapter(dataAdapter);
	}

	public void showDateTimePicker() {
		DateTimePickerDialog dtpDialog = new DateTimePickerDialog(this.getActivity());

		dtpDialog.setIcon(R.drawable.calendario);
		Calendar c = Calendar.getInstance();

		dtpDialog.setDateTime(c);

		dtpDialog.setButton(AlertDialog.BUTTON_POSITIVE, "Salvar", dialog_onclick);

		dtpDialog.show();
	}
	
	@Override
	public void onCreateContextMenu(ContextMenu menu, View v,
	    ContextMenuInfo menuInfo) {
	  if (v.getId()==R.id.listAgendamentos) {
	    //AdapterView.AdapterContextMenuInfo info = (AdapterView.AdapterContextMenuInfo)menuInfo;
	    menu.setHeaderTitle("O que deseja fazer?");
	    
	    for (int i = 0; i<menuItems.length; i++) {
	      menu.add(Menu.NONE, i, i, menuItems[i]);
	    }
	  }
	}
	
	@Override
	public boolean onContextItemSelected(MenuItem item) {
	  AdapterView.AdapterContextMenuInfo info = (AdapterView.AdapterContextMenuInfo)item.getMenuInfo();
	  //int menuItemIndex = item.getItemId();
	  
	  //String menuItemName = menuItems[menuItemIndex];
	  //String codigo = listaVisualizacao.get(info.position).get("Codigo");
	  
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

	DialogInterface.OnClickListener dialog_onclick = new DialogInterface.OnClickListener() {

		@Override
		public void onClick(DialogInterface dialog, int which) {
			try {
				if (dialog.getClass() != DateTimePickerDialog.class) {
					return;
				}
				switch (which) {
				case DialogInterface.BUTTON_POSITIVE:
					DateTimePickerDialog reminderDl = (DateTimePickerDialog) dialog;

					Date date = reminderDl.getDate();

					if (identificador == 1) {
						lblDataHoraInicial.setText(Helper.dateToString(date, Helper.NORMAL_FORMAT));
						dataHoraInicial = date;
					} else {
						lblDataHoraFinal.setText(Helper.dateToString(date, Helper.NORMAL_FORMAT));
						dataHoraFinal = date;
					}
					break;
				default:
					break;
				}
			} catch (Exception ex) {
				Log.e("ControleAgendamento", ex.getMessage());
			}
		}
	};
}
