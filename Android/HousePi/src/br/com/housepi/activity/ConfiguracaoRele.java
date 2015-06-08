package br.com.housepi.activity;

import java.util.ArrayList;
import java.util.List;

import org.jdom2.Attribute;
import org.jdom2.Document;
import org.jdom2.Element;
import org.jdom2.output.XMLOutputter;

import br.com.housepi.R;
import br.com.housepi.classes.Conexao;
import br.com.housepi.classes.Funcoes;
import br.com.housepi.classes.Rele;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.EditText;

public class ConfiguracaoRele extends Fragment implements OnClickListener {
	private EditText edtNomeRele0;
	private EditText edtNomeRele1;
	private EditText edtNomeRele2;
	private EditText edtNomeRele3;
	private EditText edtNomeRele4;
	private EditText edtNomeRele5;
	private EditText edtNomeRele6;
	private EditText edtNomeRele7;
	private EditText edtNomeRele8;
	private EditText edtNomeRele9;
	private CheckBox cbxRele0;
	private CheckBox cbxRele1;
	private CheckBox cbxRele2;
	private CheckBox cbxRele3;
	private CheckBox cbxRele4;
	private CheckBox cbxRele5;
	private CheckBox cbxRele6;
	private CheckBox cbxRele7;
	private CheckBox cbxRele8;
	private CheckBox cbxRele9;
		private Button btnSalvar;
	
	@Override
	public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
		
		View rootView = inflater.inflate(R.layout.configuracao_rele, container, false);
		
		edtNomeRele0  = (EditText) rootView.findViewById(R.id.edtNomeRele0);
		edtNomeRele1  = (EditText) rootView.findViewById(R.id.edtNomeRele1);
		edtNomeRele2  = (EditText) rootView.findViewById(R.id.edtNomeRele2);
		edtNomeRele3  = (EditText) rootView.findViewById(R.id.edtNomeRele3);
		edtNomeRele4  = (EditText) rootView.findViewById(R.id.edtNomeRele4);
		edtNomeRele5  = (EditText) rootView.findViewById(R.id.edtNomeRele5);
		edtNomeRele6  = (EditText) rootView.findViewById(R.id.edtNomeRele6);
		edtNomeRele7  = (EditText) rootView.findViewById(R.id.edtNomeRele7);
		edtNomeRele8  = (EditText) rootView.findViewById(R.id.edtNomeRele8);
		edtNomeRele9  = (EditText) rootView.findViewById(R.id.edtNomeRele9);
		
		cbxRele0 = (CheckBox) rootView.findViewById(R.id.cbxRele0);
		cbxRele1 = (CheckBox) rootView.findViewById(R.id.cbxRele1);
		cbxRele2 = (CheckBox) rootView.findViewById(R.id.cbxRele2);
		cbxRele3 = (CheckBox) rootView.findViewById(R.id.cbxRele3);
		cbxRele4 = (CheckBox) rootView.findViewById(R.id.cbxRele4);
		cbxRele5 = (CheckBox) rootView.findViewById(R.id.cbxRele5);
		cbxRele6 = (CheckBox) rootView.findViewById(R.id.cbxRele6);
		cbxRele7 = (CheckBox) rootView.findViewById(R.id.cbxRele7);
		cbxRele8 = (CheckBox) rootView.findViewById(R.id.cbxRele8);
		cbxRele9 = (CheckBox) rootView.findViewById(R.id.cbxRele9);
		
		btnSalvar  = (Button) rootView.findViewById(R.id.btnSalvarConfRele);
		btnSalvar.setOnClickListener(this);
		
		getNomeAtual();
		
		return rootView;
	}
	
	public void onClick(View view) {
		if (view == btnSalvar) {
			
			if (edtNomeRele0.getText().toString().trim().equals("") || edtNomeRele1.getText().toString().trim().equals("") ||
				edtNomeRele2.getText().toString().trim().equals("") || edtNomeRele3.getText().toString().trim().equals("") ||
				edtNomeRele4.getText().toString().trim().equals("") || edtNomeRele5.getText().toString().trim().equals("") ||
				edtNomeRele6.getText().toString().trim().equals("") || edtNomeRele7.getText().toString().trim().equals("") ||
				edtNomeRele8.getText().toString().trim().equals("") || edtNomeRele9.getText().toString().trim().equals("")) {
				Funcoes.msgDialogoInformacao("Atenção", "Preencha todos os campos antes de salvar.", this.getActivity());
			} else {
				String mensagem = "";
				
				Document doc = new Document();
				Element root = new Element("AlterarConfiguracaoRele");
				
				Element rele;
				
				rele = new Element("Rele");
				rele.setAttribute(new Attribute("Id", "0"));
				rele.setAttribute(new Attribute("Nome", edtNomeRele0.getText().toString()));
				rele.setAttribute(new Attribute("Ativo", cbxRele0.isChecked()?"1":"0"));
				root.addContent(rele);
				
				rele = new Element("Rele");
				rele.setAttribute(new Attribute("Id", "1"));
				rele.setAttribute(new Attribute("Nome", edtNomeRele1.getText().toString()));
				rele.setAttribute(new Attribute("Ativo", cbxRele1.isChecked()?"1":"0"));
				root.addContent(rele);

				rele = new Element("Rele");
				rele.setAttribute(new Attribute("Id", "2"));
				rele.setAttribute(new Attribute("Nome", edtNomeRele2.getText().toString()));
				rele.setAttribute(new Attribute("Ativo", cbxRele2.isChecked()?"1":"0"));
				root.addContent(rele);

				rele = new Element("Rele");
				rele.setAttribute(new Attribute("Id", "3"));
				rele.setAttribute(new Attribute("Nome", edtNomeRele3.getText().toString()));
				rele.setAttribute(new Attribute("Ativo", cbxRele3.isChecked()?"1":"0"));
				root.addContent(rele);

				rele = new Element("Rele");
				rele.setAttribute(new Attribute("Id", "4"));
				rele.setAttribute(new Attribute("Nome", edtNomeRele4.getText().toString()));
				rele.setAttribute(new Attribute("Ativo", cbxRele4.isChecked()?"1":"0"));
				root.addContent(rele);

				rele = new Element("Rele");
				rele.setAttribute(new Attribute("Id", "5"));
				rele.setAttribute(new Attribute("Nome", edtNomeRele5.getText().toString()));
				rele.setAttribute(new Attribute("Ativo", cbxRele5.isChecked()?"1":"0"));
				root.addContent(rele);

				rele = new Element("Rele");
				rele.setAttribute(new Attribute("Id", "6"));
				rele.setAttribute(new Attribute("Nome", edtNomeRele6.getText().toString()));
				rele.setAttribute(new Attribute("Ativo", cbxRele6.isChecked()?"1":"0"));
				root.addContent(rele);

				rele = new Element("Rele");
				rele.setAttribute(new Attribute("Id", "7"));
				rele.setAttribute(new Attribute("Nome", edtNomeRele7.getText().toString()));
				rele.setAttribute(new Attribute("Ativo", cbxRele7.isChecked()?"1":"0"));
				root.addContent(rele);

				rele = new Element("Rele");
				rele.setAttribute(new Attribute("Id", "8"));
				rele.setAttribute(new Attribute("Nome", edtNomeRele8.getText().toString()));
				rele.setAttribute(new Attribute("Ativo", cbxRele8.isChecked()?"1":"0"));
				root.addContent(rele);

				rele = new Element("Rele");
				rele.setAttribute(new Attribute("Id", "9"));
				rele.setAttribute(new Attribute("Nome", edtNomeRele9.getText().toString()));
				rele.setAttribute(new Attribute("Ativo", cbxRele9.isChecked()?"1":"0"));
				root.addContent(rele);
				
				doc.setRootElement(root);
				
				mensagem = new XMLOutputter().outputString(doc);				
				Conexao.getConexaoAtual().enviarMensagem(mensagem);
				
				mensagem = Conexao.getConexaoAtual().receberRetorno();
				
				if (mensagem.equals("Ok")) {
					Funcoes.msgToastDadosGravados(this.getActivity());
				} else {
					Funcoes.msgToastErroGravar(this.getActivity());
				} 
			}
		}
	}
	
	public void getNomeAtual() {
		List<Rele> listaReles = new ArrayList<Rele>();
		
		for (int i=0;i<10;i++) {
			listaReles.add(new Rele(i));
		}
		
		Rele.getConfiguracaoStatus(listaReles);
		
		edtNomeRele0.setText(listaReles.get(0).getNome());
		edtNomeRele1.setText(listaReles.get(1).getNome());
		edtNomeRele2.setText(listaReles.get(2).getNome());
		edtNomeRele3.setText(listaReles.get(3).getNome());
		edtNomeRele4.setText(listaReles.get(4).getNome());
		edtNomeRele5.setText(listaReles.get(5).getNome());
		edtNomeRele6.setText(listaReles.get(6).getNome());
		edtNomeRele7.setText(listaReles.get(7).getNome());
		edtNomeRele8.setText(listaReles.get(8).getNome());
		edtNomeRele9.setText(listaReles.get(9).getNome());
		
		cbxRele0.setChecked(listaReles.get(0).getAtivo() == 1);
		cbxRele1.setChecked(listaReles.get(1).getAtivo() == 1);
		cbxRele2.setChecked(listaReles.get(2).getAtivo() == 1);
		cbxRele3.setChecked(listaReles.get(3).getAtivo() == 1);
		cbxRele4.setChecked(listaReles.get(4).getAtivo() == 1);
		cbxRele5.setChecked(listaReles.get(5).getAtivo() == 1);
		cbxRele6.setChecked(listaReles.get(6).getAtivo() == 1);
		cbxRele7.setChecked(listaReles.get(7).getAtivo() == 1);
		cbxRele8.setChecked(listaReles.get(8).getAtivo() == 1);
		cbxRele9.setChecked(listaReles.get(9).getAtivo() == 1);
	}
}
