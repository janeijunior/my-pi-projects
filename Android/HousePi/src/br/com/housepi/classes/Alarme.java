package br.com.housepi.classes;

import java.io.Reader;
import java.io.StringReader;
import org.jdom2.Document;
import org.jdom2.Element;
import org.jdom2.JDOMException;
import org.jdom2.input.SAXBuilder;
import org.jdom2.output.XMLOutputter;

import android.graphics.Color;
import android.widget.TextView;
import android.widget.ToggleButton;

public class Alarme {
	private Boolean alarmeLigado;
	private Boolean panicoLigado;
	private String statusAlarme;
	private ToggleButton btnAlarme;
	private ToggleButton btnPanico;
	private TextView lblStatus;
	
	public Alarme() {
		super();
		
	}

	public Alarme(ToggleButton btnAlarme, ToggleButton btnPanico,
			TextView lblStatus) {
		super();
		this.btnAlarme = btnAlarme;
		this.btnPanico = btnPanico;
		this.lblStatus = lblStatus;
	}

	public String getStatusAlarme() {
		return statusAlarme;
	}

	public void setStatusAlarme(String statusAlarme) {
		this.statusAlarme = statusAlarme;
		
		this.getLblStatus().setText(this.getStatusAlarme());
		
		if (this.getStatusAlarme().equals("Normal")) {
			this.getLblStatus().setTextColor(Color.GREEN);
		} else if (this.getStatusAlarme().equals("Disparado")) {
			this.getLblStatus().setTextColor(Color.RED);
		} else {
			this.getLblStatus().setTextColor(Color.BLACK);
		}
	}
	
	public TextView getLblStatus() {
		return lblStatus;
	}

	public void setLblStatus(TextView lblStatus) {
		this.lblStatus = lblStatus;
	}

	public ToggleButton getBtnAlarme() {
		return btnAlarme;
	}

	public void setBtnAlarme(ToggleButton btnAlarme) {
		this.btnAlarme = btnAlarme;
	}

	public ToggleButton getBtnPanico() {
		return btnPanico;
	}

	public void setBtnPanico(ToggleButton btnPanico) {
		this.btnPanico = btnPanico;
	}
	
	public Boolean getAlarmeLigado() {
		return alarmeLigado;
	}

	public void setAlarmeLigado(Boolean alarmeLigado) {
		this.alarmeLigado = alarmeLigado;
	}

	public Boolean getPanicoLigado() {
		return panicoLigado;
	}

	public void setPanicoLigado(Boolean panicoLigado) {
		this.panicoLigado = panicoLigado;
	}

	public Boolean ligarAlarme() {
		Boolean resposta = montarEnviarXMLControle("Alarme", "Ligar");	
		
		if (resposta) {
			this.setStatusAlarme("Normal");
		} 
		
		return resposta;
	}
	
	public Boolean desligarAlarme() {
		Boolean resposta = montarEnviarXMLControle("Alarme", "Desligar");
	
		if (resposta) {
			this.setStatusAlarme("Desligado");
		}
		
		return resposta;
	}
	
	public Boolean ligarPanico() {
		return montarEnviarXMLControle("Panico", "Ligar");
	}
	
	public Boolean desligarPanico() {
		return montarEnviarXMLControle("Panico", "Desligar");
	}
	
	private Boolean montarEnviarXMLControle(String funcao, String comando) {
		Document doc = new Document();
		Element root = new Element(funcao);
		       
		Element acao = new Element("Acao");	
		
		acao.setText(comando);
		
		root.addContent(acao);
		doc.setRootElement(root);
		Conexao.getConexaoAtual().enviarMensagem(new XMLOutputter().outputString(doc));
		
		if (Conexao.getConexaoAtual().receberRetorno().equals("Ok")) {
			return true;
		} else {
			return false;
		}
	}
	
	public void getConfiguracaoStatus() {
		try {
			Document doc = new Document();
			Element root = new Element("StatusAlarme");
			doc.setRootElement(root);

			Conexao.getConexaoAtual().enviarMensagem(new XMLOutputter().outputString(doc));

			String mensagem = "";

			mensagem = Conexao.getConexaoAtual().receberRetorno();

			SAXBuilder builder = new SAXBuilder();
			Reader in = new StringReader(mensagem);

			try {
				doc = builder.build(in);
			} catch (JDOMException e) {
				e.printStackTrace();
			}

			Element retorno = (Element) doc.getRootElement();
			
			this.setStatusAlarme(retorno.getChild("SensorAlarme").getAttribute("Status").getValue());
										
			this.setAlarmeLigado(retorno.getChild("SensorAlarme").getAttribute("Ligado").getIntValue() == 1);
			this.getBtnAlarme().setChecked(this.getAlarmeLigado());
			
			this.setPanicoLigado(retorno.getChild("PanicoAlarme").getAttribute("Ligado").getIntValue() == 1);
			this.getBtnPanico().setChecked(this.getPanicoLigado());
			
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

}
