# MultipleFiles/tela_historico_processos.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView, QAbstractItemView,
    QTextEdit
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from db.db import conectar

class TelaHistoricoProcessos(QWidget):
    def __init__(self, usuario_id):
        super().__init__()
        self.usuario_id = usuario_id
        self.setWindowTitle("Histórico de Processos")
        self.setFixedSize(900, 700)
        self.setStyleSheet("""
            QWidget {
                background-color: #1B3A5E;
                color: white;
                font-family: 'Segoe UI';
            }
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #FFCD00;
            }
            QPushButton {
                background-color: #FFCD00;
                color: #1B3A5E;
                font-weight: bold;
                border: none;
                padding: 12px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #e6b800;
            }
            QTableWidget {
                background-color: white;
                color: black;
                border-radius: 8px;
                font-size: 11pt;
            }
            QHeaderView::section {
                background-color: #1A2A47;
                color: #FFCD00;
                padding: 8px;
                font-weight: bold;
                font-size: 11pt;
            }
            QTableWidget::item:selected {
                background-color: #FFCD00;
                color: #1B3A5E;
            }
            QTextEdit {
                background-color: white;
                color: black;
                border-radius: 4px;
                padding: 6px;
                font-size: 13px;
            }
        """)

        self._setup_ui()
        self._carregar_historico()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        title_label = QLabel("Histórico de Processos")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)

        self.tabela_historico = QTableWidget()
        self.tabela_historico.setColumnCount(4)
        self.tabela_historico.setHorizontalHeaderLabels(["ID", "Nome do Processo", "Responsável", "Data de Início"])
        self.tabela_historico.verticalHeader().setVisible(False)
        self.tabela_historico.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tabela_historico.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tabela_historico.setAlternatingRowColors(True)
        self.tabela_historico.setColumnHidden(0, True) # Esconder a coluna ID
        header = self.tabela_historico.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.tabela_historico.itemSelectionChanged.connect(self._exibir_detalhes_processo)
        main_layout.addWidget(self.tabela_historico)

        details_layout = QVBoxLayout()
        details_layout.setSpacing(10)
        details_layout.addWidget(QLabel("Detalhes do Processo Selecionado:"))
        self.process_details_text = QTextEdit()
        self.process_details_text.setReadOnly(True)
        details_layout.addWidget(self.process_details_text)
        main_layout.addLayout(details_layout)

        self.btn_voltar = QPushButton("Voltar")
        self.btn_voltar.clicked.connect(self._voltar_tela_gerenciar_processos)
        main_layout.addWidget(self.btn_voltar, alignment=Qt.AlignmentFlag.AlignRight)

    def _carregar_historico(self):
        self.tabela_historico.setRowCount(0)
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome_processo, responsavel, data_inicio FROM formularios_processos WHERE usuario_id = ?", (self.usuario_id,))
        processos = cursor.fetchall()
        conn.close()

        if processos:
            for row_idx, processo in enumerate(processos):
                self.tabela_historico.insertRow(row_idx)
                for col_idx, data in enumerate(processo):
                    self.tabela_historico.setItem(row_idx, col_idx, QTableWidgetItem(str(data)))
        else:
            QMessageBox.information(self, "Informação", "Nenhum processo encontrado no histórico.")

    def _exibir_detalhes_processo(self):
        selected_items = self.tabela_historico.selectedItems()
        if not selected_items:
            self.process_details_text.clear()
            return

        processo_id = int(selected_items[0].text())
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM formularios_processos WHERE id = ?", (processo_id,))
        processo_detalhes = cursor.fetchone()
        conn.close()

        if processo_detalhes:
            details_str = ""
            # Mapear colunas para nomes legíveis (ajuste conforme a ordem da sua tabela formularios_processos)
            column_names = [
                "ID", "ID do Usuário", "Nome do Processo", "Responsável", "Data de Início",
                "Nome da Fase", "Ordem da Fase", "Objetivo da Fase",
                "Nome do Passo", "Ordem do Passo", "Descrição do Passo", "Ferramentas",
                "Tempo Estimado", "Riscos", "Entradas", "Saídas",
                "Depende", "Depende Qual", "Decisão", "Fluxo de Decisão",
                "Tempo Real", "Qualidade", "Lições Aprendidas", "Melhorias Sugeridas",
                "Data de Registro"
            ]
            for i, detail in enumerate(processo_detalhes):
                if i < len(column_names):
                    details_str += f"**{column_names[i]}:** {detail}\n"
                else:
                    details_str += f"**Coluna {i}:** {detail}\n" # Fallback para colunas não mapeadas
            self.process_details_text.setText(details_str)
        else:
            self.process_details_text.clear()
            QMessageBox.warning(self, "Erro", "Detalhes do processo não encontrados.")

    def _voltar_tela_gerenciar_processos(self):
        from telas.tela_gerenciar_processos import TelaGerenciarProcessos
        self.close()
        tela_gerenciar_processos = TelaGerenciarProcessos(self.usuario_id)
        tela_gerenciar_processos.show()

