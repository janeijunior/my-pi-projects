package br.com.housepi.activity;

import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.List;
import br.com.housepi.R;
import br.com.housepi.bibliotecas.DateTimePickerDialog;
import br.com.housepi.bibliotecas.Helper;
import br.com.housepi.classes.Agendamento;
import br.com.housepi.classes.Funcoes;
import br.com.housepi.classes.Rele;
import android.os.Bundle;
import android.app.AlertDialog;
import android.app.Dialog;
import android.content.DialogInterface;
import android.support.v7.app.ActionBarActivity;
import android.util.Log;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;
import android.widget.ToggleButton;

public class CadastroAgendamento extends ActionBarActivity implements OnClickListener {
	private Button btnEquipamento;
	private Button btnDefinirInicial;
	private Button btnDefinirFinal;
	private Button btnAdicionar;
	private ToggleButton btnDom;
	private ToggleButton btnSeg;
	private ToggleButton btnTer;
	private ToggleButton btnQua;
	private ToggleButton btnQui;
	private ToggleButton btnSex;
	private ToggleButton btnSab;
	private TextView lblDataHoraInicial;
	private TextView lblDataHoraFinal;
	private TextView lblEquipamento;
	private EditText edtNome;
	private Integer identificador;
	private Date dataHoraInicial;
	private Date dataHoraFinal;
	private List<String> listaOpcoes = new ArrayList<String>();
	private CharSequence[] opcoes;
	private boolean[] selecao;
	
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.cadastro_agendamento);
	
		edtNome = (EditText) findViewById(R.id.edtNomeAgendamento);
		
		btnEquipamento = (Button) findViewById(R.id.btnEquipamento);
		btnEquipamento.setOnClickListener(this);
		
		btnDefinirInicial = (Button) findViewById(R.id.btnDataHoraInicial);
		btnDefinirInicial.setOnClickListener(this);

		btnDefinirFinal = (Button) findViewById(R.id.btnDataHoraFinal);
		btnDefinirFinal.setOnClickListener(this);

		btnAdicionar = (Button) findViewById(R.id.btnAdicionar);
		btnAdicionar.setOnClickListener(this);

		btnDom = (ToggleButton) findViewById(R.id.btnDom);
		btnSeg = (ToggleButton) findViewById(R.id.btnSeg);
		btnTer = (ToggleButton) findViewById(R.id.btnTer);
		btnQua = (ToggleButton) findViewById(R.id.btnQua);
		btnQui = (ToggleButton) findViewById(R.id.btnQui);
		btnSex = (ToggleButton) findViewById(R.id.btnSex);
		btnSab = (ToggleButton) findViewById(R.id.btnSab);
		
		lblDataHoraInicial = (TextView) findViewById(R.id.lblDataHoraInicial);
		lblDataHoraFinal = (TextView) findViewById(R.id.lblDataHoraFinal);
		lblEquipamento = (TextView) findViewById(R.id.lblEquipamento);
		
		addItensLista();
	}
	
	@SuppressWarnings("deprecation")
	@Override
	public void onClick(View view) {
		if (view == btnEquipamento) {
			showDialog(0);
	    } else if (view == btnDefinirInicial) {
			identificador = 1;
			showDateTimePicker();
		} else if (view == btnDefinirFinal) {
			identificador = 2;
			showDateTimePicker();
		} else if (view == btnAdicionar) {
			if (edtNome.getText().toString().trim().equals("")) {
				Funcoes.msgDialogoInformacao("Atenção", "Informe um nome antes de continuar.", this);
			} else if (lblEquipamento.getText().equals("Definir...")) {
				Funcoes.msgDialogoInformacao("Atenção", "Selecione pelo menos um equipamento.", this);	
			} else if (dataHoraInicial == null) {
				Funcoes.msgDialogoInformacao("Atenção", "Informe a data e a hora que deseja ligar o equipamento.", this);
			} else if (dataHoraFinal == null) {
				Funcoes.msgDialogoInformacao("Atenção", "Informe a data e a hora que deseja desligar o equipamento.", this);
			} else if (dataHoraInicial.after(dataHoraFinal)) {
				Funcoes.msgDialogoInformacao("Atenção", "A data/hora de desligamento deve ser maior que a data/hora de acionamento.", this);
			} else {
				Agendamento agendamento = new Agendamento(edtNome.getText().toString().trim(), dataHoraInicial, dataHoraFinal);
				
				String equipamentos = "";
				
				for( int i = 0; i < opcoes.length; i++ ){
					if (selecao[i]) {
						Integer posicao = i - 1;
						equipamentos = equipamentos + posicao.toString() + ";";
					}
				}
				
				agendamento.setEquipamentos(equipamentos);
				
				agendamento.setDiasDaSemana(getDias());
				
				if (agendamento.gravarAgendamento()) {
					Toast.makeText(this, "Agendamento inserido com sucesso!", Toast.LENGTH_LONG).show();
				
					dataHoraInicial = null;
					dataHoraFinal = null;
					
					edtNome.getText().clear();
					lblDataHoraInicial.setText("Data e Hora");
					lblDataHoraFinal.setText("Data e Hora");
					
					finish();
				} else {
					Toast.makeText(this, "Não foi possível inserir o agendamento.", Toast.LENGTH_LONG).show();
				}
			}
		}
	}

	public void addItensLista() {
		List<Rele> listaReles = new ArrayList<Rele>();

		for (int i = 0; i < 10; i++) {
			listaReles.add(new Rele(i, null));
		}

		Rele.getConfiguracaoStatus(listaReles);

		listaOpcoes.add("Alarme");

		for (Rele rele : listaReles) {
			listaOpcoes.add(rele.getNome());
		}
		
		opcoes = listaOpcoes.toArray(new CharSequence[listaOpcoes.size()]);
		selecao = new boolean[opcoes.length ];
	}
	
	private String getDias() {
		String dias = "";
		
		if (btnDom.isChecked()) {
			dias = dias + "0;";
		} 
		if (btnSeg.isChecked()) {
			dias = dias + "1;";
		} 
		if (btnTer.isChecked()) {
			dias = dias + "2;";
		} 
		if (btnQua.isChecked()) {
			dias = dias + "3;";
		}
		if (btnQui.isChecked()) {
			dias = dias + "4;";
		}
		if (btnSex.isChecked()) {
			dias = dias + "5;";
		} 
		if (btnSab.isChecked()) {
			dias = dias + "6;";
		}
		
		return dias;
	}

	public void showDateTimePicker() {
		DateTimePickerDialog dtpDialog = new DateTimePickerDialog(this);

		dtpDialog.setIcon(R.drawable.ic_calendario);
		Calendar c = Calendar.getInstance();

		dtpDialog.setDateTime(c);

		dtpDialog.setButton(AlertDialog.BUTTON_POSITIVE, "Ok", dialog_onclick);

		dtpDialog.show();
	}
	
	
	@Override
	protected Dialog onCreateDialog( int id ) 
	{
		return 
		new AlertDialog.Builder(this)
        	.setTitle( "Equipamentos" )
        	.setMultiChoiceItems(opcoes, selecao, new DialogSelectionClickHandler() )
        	.setPositiveButton("Ok", new DialogButtonClickHandler() )
        	.create();
	}
	
	
	public class DialogSelectionClickHandler implements DialogInterface.OnMultiChoiceClickListener
	{
		public void onClick( DialogInterface dialog, int clicked, boolean selected )
		{
			atualizarLabelSelecionados();
		}
	}
	

	public class DialogButtonClickHandler implements DialogInterface.OnClickListener
	{
		public void onClick( DialogInterface dialog, int clicked )
		{
			switch( clicked )
			{
				case DialogInterface.BUTTON_POSITIVE:
					atualizarLabelSelecionados();
					break;
			}
		}
	}
	
	protected void atualizarLabelSelecionados(){
		String selecionado = "";
		
		for( int i = 0; i < opcoes.length; i++ ){
			if (selecao[i]) {
				if (selecionado.equals("")) {
					selecionado = opcoes[i].toString();
				} else {
					selecionado = selecionado + ", " + opcoes[i];
				}
			}
		}
		if (selecionado.equals("")) {
			lblEquipamento.setText("Definir...");
		} else {
			lblEquipamento.setText(selecionado);
		}
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
				Log.e("CadastroAgendamento", ex.getMessage());
			}
		}
	};

}
