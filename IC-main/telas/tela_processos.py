from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton,
    QStackedWidget, QHBoxLayout, QMessageBox
)
from PyQt6.QtCore import pyqtSignal
from db.db import conectar

class TelaProcessos(QWidget):
    deve_retornar = pyqtSignal()

    def __init__(self, usuario_id, processo_id=None):
        super().__init__()
        self.usuario_id = usuario_id
        self.processo_id = processo_id
        self.setWindowTitle("Formulário de Processo")
        self.setFixedSize(800, 600)
        self.setStyleSheet("""
            QWidget {
                background-color: #1B3A5E;
                color: white;
                font-family: 'Segoe UI';
            }
            QLabel {
                font-size: 14px;
                margin-top: 8px;
            }
            QTextEdit {
                background-color: white;
                color: black;
                border-radius: 4px;
                padding: 6px;
                font-size: 13px;
            }
            QPushButton {
                background-color: #FFCD00;
                color: #1B3A5E;
                font-weight: bold;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #e6b800;
            }
        """)

        self.stack = QStackedWidget()
        self.page_identificacao = QWidget()
        self.page_fase = QWidget()
        self.page_passo = QWidget()
        self.page_dependencias = QWidget()
        self.page_avaliacao = QWidget()
        self.page_confirmacao = QWidget()

        self.init_identificacao()
        self.init_fase()
        self.init_passo()
        self.init_dependencias()
        self.init_avaliacao()
        self.init_confirmacao()

        self.stack.addWidget(self.page_identificacao)
        self.stack.addWidget(self.page_fase)
        self.stack.addWidget(self.page_passo)
        self.stack.addWidget(self.page_dependencias)
        self.stack.addWidget(self.page_avaliacao)
        self.stack.addWidget(self.page_confirmacao)

        layout = QVBoxLayout()
        layout.addWidget(self.stack)

        nav = QHBoxLayout()
        self.btn_voltar = QPushButton("← Voltar")
        self.btn_avancar = QPushButton("Avançar →")
        self.btn_salvar_rascunho = QPushButton("Salvar Rascunho")
        self.btn_voltar.clicked.connect(self.voltar)
        self.btn_avancar.clicked.connect(self.avancar)
        self.btn_salvar_rascunho.clicked.connect(self.salvar_rascunho_com_msg)
        nav.addWidget(self.btn_voltar)
        nav.addWidget(self.btn_salvar_rascunho)
        nav.addWidget(self.btn_avancar)

        layout.addLayout(nav)
        self.setLayout(layout)

        if self.processo_id:
            self._carregar_dados_processo()

    def init_identificacao(self):
        layout = QVBoxLayout(self.page_identificacao)
        self.inp_nome_processo = QTextEdit()
        self.inp_responsavel = QTextEdit()
        self.inp_data_inicio = QTextEdit()
        layout.addWidget(QLabel("Nome do Processo*"))
        layout.addWidget(self.inp_nome_processo)
        layout.addWidget(QLabel("Responsável*"))
        layout.addWidget(self.inp_responsavel)
        layout.addWidget(QLabel("Data de Início*"))
        layout.addWidget(self.inp_data_inicio)

    def init_fase(self):
        layout = QVBoxLayout(self.page_fase)
        self.inp_nome_fase = QTextEdit()
        self.inp_ordem_fase = QTextEdit()
        self.inp_objetivo_fase = QTextEdit()
        layout.addWidget(QLabel("Nome da Fase*"))
        layout.addWidget(self.inp_nome_fase)
        layout.addWidget(QLabel("Ordem da Fase*"))
        layout.addWidget(self.inp_ordem_fase)
        layout.addWidget(QLabel("Objetivo da Fase*"))
        layout.addWidget(self.inp_objetivo_fase)

    def init_passo(self):
        layout = QVBoxLayout(self.page_passo)
        self.inp_nome_passo = QTextEdit()
        self.inp_ordem_passo = QTextEdit()
        self.inp_desc_passo = QTextEdit()
        self.inp_ferramentas = QTextEdit()
        self.inp_tempo_estimado = QTextEdit()
        self.inp_riscos = QTextEdit()
        self.inp_entradas = QTextEdit()
        self.inp_saidas = QTextEdit()
        layout.addWidget(QLabel("Nome do Passo*"))
        layout.addWidget(self.inp_nome_passo)
        layout.addWidget(QLabel("Ordem do Passo*"))
        layout.addWidget(self.inp_ordem_passo)
        layout.addWidget(QLabel("Descrição do Passo*"))
        layout.addWidget(self.inp_desc_passo)
        layout.addWidget(QLabel("Ferramentas ou Recursos Utilizados*"))
        layout.addWidget(self.inp_ferramentas)
        layout.addWidget(QLabel("Tempo Estimado*"))
        layout.addWidget(self.inp_tempo_estimado)
        layout.addWidget(QLabel("Riscos Possíveis*"))
        layout.addWidget(self.inp_riscos)
        layout.addWidget(QLabel("Entradas Necessárias*"))
        layout.addWidget(self.inp_entradas)
        layout.addWidget(QLabel("Saídas Esperadas*"))
        layout.addWidget(self.inp_saidas)

    def init_dependencias(self):
        layout = QVBoxLayout(self.page_dependencias)
        self.inp_depende = QTextEdit()
        self.inp_depende_qual = QTextEdit()
        self.inp_decisao = QTextEdit()
        self.inp_fluxo_decisao = QTextEdit()
        layout.addWidget(QLabel("Este passo depende de outro?*"))
        layout.addWidget(self.inp_depende)
        layout.addWidget(QLabel("Se sim, qual?"))
        layout.addWidget(self.inp_depende_qual)
        layout.addWidget(QLabel("Este passo leva a uma decisão?*"))
        layout.addWidget(self.inp_decisao)
        layout.addWidget(QLabel("Fluxo de Decisão"))
        layout.addWidget(self.inp_fluxo_decisao)

    def init_avaliacao(self):
        layout = QVBoxLayout(self.page_avaliacao)
        self.inp_tempo_real = QTextEdit()
        self.inp_qualidade = QTextEdit()
        self.inp_licoes = QTextEdit()
        self.inp_melhorias = QTextEdit()
        layout.addWidget(QLabel("Tempo Real Gasto*"))
        layout.addWidget(self.inp_tempo_real)
        layout.addWidget(QLabel("Qualidade da Saída (1 a 10)*"))
        layout.addWidget(self.inp_qualidade)
        layout.addWidget(QLabel("Lições Aprendidas"))
        layout.addWidget(self.inp_licoes)
        layout.addWidget(QLabel("Melhorias Sugeridas"))
        layout.addWidget(self.inp_melhorias)

    def init_confirmacao(self):
        layout = QVBoxLayout(self.page_confirmacao)
        self.lbl_confirmacao = QLabel("Clique em Avançar novamente para salvar.")
        layout.addWidget(self.lbl_confirmacao)

    def _carregar_dados_processo(self):
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM formularios_processos WHERE id = ?", (self.processo_id,))
            dados = cursor.fetchone()
            conn.close()

            if dados:
                self.inp_nome_processo.setText(str(dados[2] or ''))
                self.inp_responsavel.setText(str(dados[3] or ''))
                self.inp_data_inicio.setText(str(dados[4] or ''))
                self.inp_nome_fase.setText(str(dados[5] or ''))
                self.inp_ordem_fase.setText(str(dados[6] or ''))
                self.inp_objetivo_fase.setText(str(dados[7] or ''))
                self.inp_nome_passo.setText(str(dados[8] or ''))
                self.inp_ordem_passo.setText(str(dados[9] or ''))
                self.inp_desc_passo.setText(str(dados[10] or ''))
                self.inp_ferramentas.setText(str(dados[11] or ''))
                self.inp_tempo_estimado.setText(str(dados[12] or ''))
                self.inp_riscos.setText(str(dados[13] or ''))
                self.inp_entradas.setText(str(dados[14] or ''))
                self.inp_saidas.setText(str(dados[15] or ''))
                self.inp_depende.setText(str(dados[16] or ''))
                self.inp_depende_qual.setText(str(dados[17] or ''))
                self.inp_decisao.setText(str(dados[18] or ''))
                self.inp_fluxo_decisao.setText(str(dados[19] or ''))
                self.inp_tempo_real.setText(str(dados[20] or ''))
                self.inp_qualidade.setText(str(dados[21] or ''))
                self.inp_licoes.setText(str(dados[22] or ''))
                self.inp_melhorias.setText(str(dados[23] or ''))
            else:
                QMessageBox.warning(self, "Erro", "Processo não encontrado para edição.")
                self.close()
        except Exception as e:
            QMessageBox.critical(self, "Erro Crítico", f"Falha ao carregar dados do processo:\n{e}")
            self.close()

    def voltar(self):
        index = self.stack.currentIndex()
        if index > 0:
            self.stack.setCurrentIndex(index - 1)
        else:
            self.deve_retornar.emit()

    def avancar(self):
        self.salvar_rascunho()  # salvamento automático sem mostrar mensagem
        index = self.stack.currentIndex()
        if index < self.stack.count() - 1:
            self.stack.setCurrentIndex(index + 1)
        else:
            self.salvar_dados()

    def salvar_rascunho(self):
        dados = (
            self.usuario_id,
            self.inp_nome_processo.toPlainText(),
            self.inp_responsavel.toPlainText(),
            self.inp_data_inicio.toPlainText(),
            self.inp_nome_fase.toPlainText(),
            self.inp_ordem_fase.toPlainText(),
            self.inp_objetivo_fase.toPlainText(),
            self.inp_nome_passo.toPlainText(),
            self.inp_ordem_passo.toPlainText(),
            self.inp_desc_passo.toPlainText(),
            self.inp_ferramentas.toPlainText(),
            self.inp_tempo_estimado.toPlainText(),
            self.inp_riscos.toPlainText(),
            self.inp_entradas.toPlainText(),
            self.inp_saidas.toPlainText(),
            self.inp_depende.toPlainText(),
            self.inp_depende_qual.toPlainText(),
            self.inp_decisao.toPlainText(),
            self.inp_fluxo_decisao.toPlainText(),
            self.inp_tempo_real.toPlainText(),
            self.inp_qualidade.toPlainText(),
            self.inp_licoes.toPlainText(),
            self.inp_melhorias.toPlainText()
        )
        conn = conectar()
        cursor = conn.cursor()
        if self.processo_id:
            cursor.execute("""
                UPDATE formularios_processos SET
                    usuario_id = ?, nome_processo = ?, responsavel = ?, data_inicio = ?,
                    nome_fase = ?, ordem_fase = ?, objetivo_fase = ?,
                    nome_passo = ?, ordem_passo = ?, descricao_passo = ?, ferramentas = ?,
                    tempo_estimado = ?, riscos = ?, entradas = ?, saidas = ?,
                    depende = ?, depende_qual = ?, decisao = ?, fluxo_decisao = ?,
                    tempo_real = ?, qualidade = ?, licoes = ?, melhorias = ?
                WHERE id = ?
            """, dados + (self.processo_id,))
        else:
            cursor.execute("""
                INSERT INTO formularios_processos (
                    usuario_id, nome_processo, responsavel, data_inicio,
                    nome_fase, ordem_fase, objetivo_fase,
                    nome_passo, ordem_passo, descricao_passo, ferramentas,
                    tempo_estimado, riscos, entradas, saidas,
                    depende, depende_qual, decisao, fluxo_decisao,
                    tempo_real, qualidade, licoes, melhorias
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, dados)
            self.processo_id = cursor.lastrowid
        conn.commit()
        conn.close()

    def salvar_rascunho_com_msg(self):
        self.salvar_rascunho()
        QMessageBox.information(self, "Rascunho salvo", "Rascunho salvo com sucesso.")

    def salvar_dados(self):
        self.salvar_rascunho()
        resposta = QMessageBox.question(
            self,
            "Ir para outra tela",
            "Deseja voltar para a tela inicial?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if resposta == QMessageBox.StandardButton.Yes:
            from telas.tela_usuario import tela_usuario
            self.close()
            tela_usuario(self.usuario_id)