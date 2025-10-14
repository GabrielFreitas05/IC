from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
    QHBoxLayout, QLineEdit, QLabel, QMessageBox, QWidget, QComboBox, QFrame,
    QSpacerItem, QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from db.db import (
    excluir_usuario, excluir_teste, listar_usuarios, listar_pta, listar_testes,
    listar_pedidos_pendentes, aprovar_pedido, rejeitar_pedido
)

# ----------------- componentes visuais (somente UI) -----------------
class SectionCard(QWidget):
    def __init__(self, title: str = "", parent=None):
        super().__init__(parent)
        self.setObjectName("SectionCard")
        v = QVBoxLayout(self)
        v.setContentsMargins(16, 16, 16, 16)
        v.setSpacing(12)

        if title:
            lab = QLabel(title)
            lab.setObjectName("SectionTitle")
            v.addWidget(lab)

        self.body = QVBoxLayout()
        self.body.setContentsMargins(0, 0, 0, 0)
        self.body.setSpacing(8)
        v.addLayout(self.body)


class Separator(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("Separator")
        self.setFrameShape(QFrame.Shape.HLine)
        self.setFixedHeight(1)


# ----------------- tela principal -----------------
class TelaAdmin(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Painel do Administrador")
        self.setFixedSize(980, 680)
        self.current_tipo = None  # guarda o que está listado no momento

        self.setStyleSheet("""
            QDialog, QWidget {
                background-color: #0B1220;
                color: #E6EAF2;
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
            }
            #Header {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                            stop:0 #0B1220, stop:1 #121B30);
                border-bottom: 1px solid #1F2A44;
            }
            #HeaderTitle {
                color: #FFCD00;
                font-size: 22px;
                font-weight: 800;
                letter-spacing: 0.3px;
            }
            #HeaderSubtitle {
                color: #9AA4BF;
                font-size: 12px;
            }
            #SectionCard {
                background-color: #0F172A;
                border: 1px solid #1F2A44;
                border-radius: 12px;
            }
            #SectionTitle {
                font-size: 13px;
                font-weight: 700;
                color: #A9B3C9;
                text-transform: uppercase;
                letter-spacing: 0.6px;
            }
            QPushButton {
                background-color: #FFCD00;
                color: #0B1220;
                font-weight: 700;
                border: 1px solid #FFDA3D;
                padding: 10px 14px;
                border-radius: 10px;
            }
            QPushButton:hover { background-color: #FFD940; }
            QPushButton:pressed { background-color: #E8BC00; }

            /* variantes */
            .ghost {
                background-color: transparent;
                color: #E6EAF2;
                border: 1px solid #2A3B63;
            }
            .ghost:hover { background-color: #122041; }
            .ghost:pressed { background-color: #0F1A36; }

            .danger {
                background-color: transparent;
                color: #FF8787;
                border: 1px solid #5A2C37;
            }
            .danger:hover { background-color: #2A1320; }
            .danger:pressed { background-color: #211019; }

            QLineEdit, QComboBox {
                background-color: #0B1220;
                border: 1px solid #24314F;
                border-radius: 10px;
                padding: 10px 12px;
                color: #E6EAF2;
                selection-background-color: #233360;
            }
            QLineEdit:focus, QComboBox:focus { border: 1px solid #FFCD00; }

            QTableWidget {
                background-color: #0B1220;
                alternate-background-color: #0E1628;
                border: 1px solid #1F2A44;
                border-radius: 10px;
                gridline-color: #1F2A44;
            }
            QTableWidget::item { padding: 6px; }
            QTableWidget::item:selected {
                background-color: #1A2A4A;
                color: #FFFFFF;
            }
            QHeaderView::section {
                background-color: #0F172A;
                color: #CBD5E1;
                padding: 10px;
                border: none;
                border-bottom: 1px solid #1F2A44;
                font-weight: 800;
                text-transform: uppercase;
                font-size: 12px;
                letter-spacing: 0.6px;
            }
            #Separator { background-color: #1F2A44; }
        """)

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 24)
        root.setSpacing(16)

        header = QWidget(objectName="Header")
        h = QVBoxLayout(header)
        h.setContentsMargins(20, 16, 20, 16)
        h.setSpacing(4)
        title_label = QLabel("Painel Administrativo", objectName="HeaderTitle")
        subtitle_label = QLabel("Gerencie usuários, PTAs, testes e pendências de cadastro",
                               objectName="HeaderSubtitle")
        h.addWidget(title_label)
        h.addWidget(subtitle_label)
        root.addWidget(header)
        root.addWidget(Separator())

        # linha de listagens + pendências
        actions_row = QHBoxLayout()
        actions_row.setSpacing(16)

        card_listagens = SectionCard("Listagens")
        row_btns = QHBoxLayout()
        row_btns.setSpacing(10)
        btn_listar_usuarios = QPushButton("Listar Usuários")
        btn_listar_usuarios.clicked.connect(self.listar_usuarios)
        btn_listar_ptas = QPushButton("Listar PTAs")
        btn_listar_ptas.clicked.connect(self.listar_ptas)
        btn_listar_testes = QPushButton("Listar Testes")
        btn_listar_testes.clicked.connect(self.listar_testes)
        row_btns.addWidget(btn_listar_usuarios)
        row_btns.addWidget(btn_listar_ptas)
        row_btns.addWidget(btn_listar_testes)
        row_btns.addItem(QSpacerItem(10, 1, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        card_listagens.body.addLayout(row_btns)
        actions_row.addWidget(card_listagens)

        card_pend = SectionCard("Fluxo de aprovação")
        btn_pendencias = QPushButton("Pendências de Cadastro")
        btn_pendencias.clicked.connect(self.abrir_pendencias)
        card_pend.body.addWidget(btn_pendencias)
        actions_row.addWidget(card_pend)

        root.addLayout(actions_row)

        # “exclusões” por ID (mantido, caso queira usar)
        excluir_card = SectionCard("Exclusões")
        excluir_row = QHBoxLayout()
        excluir_row.setSpacing(10)
        self.usuario_id_input = QLineEdit()
        self.usuario_id_input.setPlaceholderText("ID do Usuário ou Teste para excluir")
        btn_excluir_usuario = QPushButton("Excluir Usuário")
        btn_excluir_usuario.clicked.connect(self.excluir_usuario)
        btn_excluir_teste = QPushButton("Excluir Teste")
        btn_excluir_teste.clicked.connect(self.excluir_teste)
        excluir_row.addWidget(self.usuario_id_input, stretch=2)
        excluir_row.addWidget(btn_excluir_usuario)
        excluir_row.addWidget(btn_excluir_teste)
        excluir_card.body.addLayout(excluir_row)
        root.addWidget(excluir_card)

        # tabela
        table_card = SectionCard("Resultados")
        self.tabela = QTableWidget()
        self.tabela.setAlternatingRowColors(True)
        self.tabela.verticalHeader().setVisible(False)
        self.tabela.horizontalHeader().setStretchLastSection(True)
        table_card.body.addWidget(self.tabela)
        root.addWidget(table_card)

        self.setLayout(root)

    # ----------------- funcionalidades originais (inalteradas) -----------------
    def listar_usuarios(self):
        usuarios = listar_usuarios()
        self.current_tipo = "Usuários"
        if usuarios:
            self.mostrar_dados(usuarios, "Usuários", ["ID", "Email", "Nome", "Senha"])
        else:
            QMessageBox.information(self, "Aviso", "Nenhum usuário encontrado.")

    def listar_ptas(self):
        ptas = listar_pta()
        self.current_tipo = "PTAs"
        if ptas:
            self.mostrar_dados(ptas, "PTAs", ["ID", "Data", "Descrição"])
        else:
            QMessageBox.information(self, "Aviso", "Nenhum PTA encontrado.")

    def listar_testes(self):
        testes = listar_testes()
        self.current_tipo = "Testes"
        if testes:
            self.mostrar_dados(testes, "Testes", ["ID", "Título", "Código", "Responsável"])
        else:
            QMessageBox.information(self, "Aviso", "Nenhum teste encontrado.")

    # --------- tabela com coluna de ações (design) ---------
    def mostrar_dados(self, dados, tipo, colunas):
        # adiciona coluna "Ações" no fim
        show_actions = tipo in ("Usuários", "Testes", "PTAs")
        headers = colunas + (["Ações"] if show_actions else [])
        self.tabela.setColumnCount(len(headers))
        self.tabela.setRowCount(len(dados))
        self.tabela.setHorizontalHeaderLabels(headers)

        for row_idx, row in enumerate(dados):
            for col_idx, valor in enumerate(row):
                item = QTableWidgetItem(str(valor))
                item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
                self.tabela.setItem(row_idx, col_idx, item)

            if show_actions:
                # cria célula com botões
                cell = QWidget()
                lay = QHBoxLayout(cell)
                lay.setContentsMargins(0, 0, 0, 0)
                lay.setSpacing(8)

                btn_edit = QPushButton("Alterar")
                btn_edit.setProperty("class", "ghost")
                btn_delete = QPushButton("Excluir")
                btn_delete.setProperty("class", "danger")

                # pega ID da primeira coluna da linha
                try:
                    row_id = int(self.tabela.item(row_idx, 0).text())
                except Exception:
                    row_id = None

                # conexões (não mexe em assinaturas do seu backend)
                btn_edit.clicked.connect(lambda _, _id=row_id: self._on_edit(_id))
                if tipo == "Usuários":
                    btn_delete.clicked.connect(lambda _, _id=row_id: self._on_delete_user(_id))
                elif tipo == "Testes":
                    btn_delete.clicked.connect(lambda _, _id=row_id: self._on_delete_test(_id))
                else:
                    # PTAs: sem função de exclusão no código original → desativa
                    btn_delete.setEnabled(False)
                    btn_delete.setToolTip("Exclusão de PTA não disponível no código original.")
                    btn_edit.setEnabled(False)
                    btn_edit.setToolTip("Edição de PTA não disponível no código original.")

                lay.addWidget(btn_edit)
                lay.addWidget(btn_delete)
                lay.addStretch(1)
                self.tabela.setCellWidget(row_idx, len(headers) - 1, cell)

        self.tabela.resizeColumnsToContents()

    # Botões de ação por linha (design → chama suas funções existentes)
    def _on_delete_user(self, user_id):
        if not user_id:
            return
        confirm = QMessageBox.question(self, "Confirmar", f"Excluir o usuário {user_id}?")
        if confirm != QMessageBox.StandardButton.Yes:
            return
        try:
            excluir_usuario(user_id)
            QMessageBox.information(self, "Sucesso", f"Usuário {user_id} excluído.")
            self.listar_usuarios()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao excluir usuário: {e}")

    def _on_delete_test(self, test_id):
        if not test_id:
            return
        confirm = QMessageBox.question(self, "Confirmar", f"Excluir o teste {test_id}?")
        if confirm != QMessageBox.StandardButton.Yes:
            return
        try:
            excluir_teste(test_id)
            QMessageBox.information(self, "Sucesso", f"Teste {test_id} excluído.")
            self.listar_testes()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao excluir teste: {e}")

    def _on_edit(self, item_id):
        # placeholder visual para não alterar backend:
        QMessageBox.information(self, "Alterar", f"Ação de alterar (ID {item_id}) – apenas UI por enquanto.")

    # ---------- botões “exclusões por ID” (mantidos do seu original) ----------
    def excluir_usuario(self):
        usuario_id = self.usuario_id_input.text()
        if usuario_id:
            try:
                excluir_usuario(usuario_id)
                QMessageBox.information(self, "Sucesso", f"Usuário {usuario_id} excluído com sucesso.")
                self.listar_usuarios()
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao excluir usuário: {e}")
        else:
            QMessageBox.warning(self, "Aviso", "Por favor, insira um ID de usuário.")

    def excluir_teste(self):
        teste_id = self.usuario_id_input.text()
        if teste_id:
            try:
                excluir_teste(teste_id)
                QMessageBox.information(self, "Sucesso", f"Teste {teste_id} excluído com sucesso.")
                self.listar_testes()
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao excluir teste: {e}")
        else:
            QMessageBox.warning(self, "Aviso", "Por favor, insira um ID de teste.")

    def abrir_pendencias(self):
        dlg = DialogPendencias(self)
        dlg.exec()


# ----------------- diálogo de pendências (design igual ao anterior bonito) -----------------
class DialogPendencias(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Pendências de Cadastro")
        self.setFixedSize(980, 600)
        self.setStyleSheet("""
            QDialog { background-color: #0B1220; color: white; font-family: 'Segoe UI', sans-serif; }
            QPushButton { background-color: #FFCD00; color: #0B1220; font-weight: 700; border: 1px solid #FFDA3D; padding: 10px 14px; border-radius: 10px; }
            QPushButton:hover { background-color: #FFD940; }
            QPushButton:pressed { background-color: #E8BC00; }
            QLineEdit, QComboBox { background-color: #0B1220; border: 1px solid #24314F; border-radius: 10px; padding: 10px 12px; color: white; }
            QLineEdit:focus, QComboBox:focus { border: 1px solid #FFCD00; }
            QTableWidget { background-color: #0B1220; color: white; border: 1px solid #1F2A44; border-radius: 10px; }
            QHeaderView::section { background-color: #0F172A; color: #CBD5E1; padding: 10px; border: none; border-bottom: 1px solid #1F2A44; font-weight: 800; text-transform: uppercase; font-size: 12px; letter-spacing: 0.6px; }
        """)

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 24)
        root.setSpacing(16)

        titulo = QLabel("Pedidos Pendentes")
        titulo.setObjectName("HeaderTitle")
        titulo.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        titulo.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        root.addWidget(titulo)

        card_table = SectionCard()
        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(["ID", "Nome", "E-mail", "ID Pers.", "Nível solicitado", "Criado em"])
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setAlternatingRowColors(True)
        card_table.body.addWidget(self.table)
        root.addWidget(card_table)

        form_card = SectionCard("Detalhes / Ação")
        form = QHBoxLayout()
        form.setSpacing(10)

        self.id_input = QLineEdit(placeholderText="ID do pedido")
        self.nome_edit = QLineEdit(placeholderText="Nome")
        self.email_edit = QLineEdit(placeholderText="E-mail")
        self.idp_edit = QLineEdit(placeholderText="ID personalizada")
        self.role_edit = QComboBox()
        self.role_edit.addItems(["user", "tech", "admin"])

        form.addWidget(self.id_input)
        form.addWidget(self.nome_edit)
        form.addWidget(self.email_edit)
        form.addWidget(self.idp_edit)
        form.addWidget(self.role_edit)

        form_card.body.addLayout(form)

        actions = QHBoxLayout()
        actions.setSpacing(10)
        btn_refresh = QPushButton("Atualizar")
        btn_load = QPushButton("Carregar seleção")
        btn_aprovar = QPushButton("Aprovar")
        btn_rejeitar = QPushButton("Rejeitar")

        actions.addWidget(btn_refresh)
        actions.addWidget(btn_load)
        actions.addItem(QSpacerItem(10, 1, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        actions.addWidget(btn_aprovar)
        actions.addWidget(btn_rejeitar)

        form_card.body.addLayout(actions)
        root.addWidget(form_card)

        btn_refresh.clicked.connect(self.load_data)
        btn_load.clicked.connect(self.load_from_selection)
        btn_aprovar.clicked.connect(self.aprovar)
        btn_rejeitar.clicked.connect(self.rejeitar)

        self.setLayout(root)
        self.load_data()

    # funcionalidades originais
    def load_data(self):
        rows = listar_pedidos_pendentes()
        self.table.setRowCount(0)
        for r in rows:
            i = self.table.rowCount()
            self.table.insertRow(i)
            self.table.setItem(i, 0, QTableWidgetItem(str(r["id"])))
            self.table.setItem(i, 1, QTableWidgetItem(r["nome"]))
            self.table.setItem(i, 2, QTableWidgetItem(r["email"]))
            self.table.setItem(i, 3, QTableWidgetItem(r["id_personalizada"]))
            self.table.setItem(i, 4, QTableWidgetItem(r["requested_role"]))
            self.table.setItem(i, 5, QTableWidgetItem(str(r["created_at"])))
        self.table.resizeColumnsToContents()

    def load_from_selection(self):
        row = self.table.currentRow()
        if row < 0:
            return
        self.id_input.setText(self.table.item(row, 0).text())
        self.nome_edit.setText(self.table.item(row, 1).text())
        self.email_edit.setText(self.table.item(row, 2).text())
        self.idp_edit.setText(self.table.item(row, 3).text())
        role = self.table.item(row, 4).text()
        idx = self.role_edit.findText(role)
        self.role_edit.setCurrentIndex(idx if idx >= 0 else 0)

    def aprovar(self):
        pid = self.id_input.text().strip()
        if not pid:
            return
        ok = aprovar_pedido(
            int(pid),
            role_final=self.role_edit.currentText(),
            email_override=self.email_edit.text().strip(),
            nome_override=self.nome_edit.text().strip(),
            idp_override=self.idp_edit.text().strip()
        )
        if ok:
            QMessageBox.information(self, "Aprovado", "Cadastro aprovado e usuário criado/ativado.")
            self.load_data()
        else:
            QMessageBox.critical(self, "Erro", "Não foi possível aprovar este pedido.")

    def rejeitar(self):
        pid = self.id_input.text().strip()
        if not pid:
            return
        if rejeitar_pedido(int(pid)):
            QMessageBox.information(self, "Rejeitado", "Pedido rejeitado.")
            self.load_data()
        else:
            QMessageBox.critical(self, "Erro", "Não foi possível rejeitar este pedido.")
