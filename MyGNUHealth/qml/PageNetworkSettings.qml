import QtQuick 2.7
import org.kde.kirigami 2.5 as Kirigami
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.3
import NetworkSettings 0.1


Kirigami.Page
{
id: phrpage
title: qsTr("Network Settings")
    NetworkSettings { // Settings object registered at main.py
        id: network_settings
        onSetOK: {
            pageStack.pop() // Return to main PHR page
        }
    }

    Kirigami.FormLayout {
        id: content
        anchors.fill: parent

        TextField {
            id: txtFederationProtocol
            placeholderText: qsTr("Protocol")
            horizontalAlignment: TextInput.AlignHCenter
         }

        TextField {
            id: txtFederationServer
            placeholderText: qsTr("Server")
            horizontalAlignment: TextInput.AlignHCenter
         }

        TextField {
            id: txtFederationPort
            placeholderText: qsTr("Port")
            horizontalAlignment: TextInput.AlignHCenter
         }

        TextField {
           id: txtFederationAccount
            placeholderText: qsTr("Federation ID")
            horizontalAlignment: TextInput.AlignHCenter
        }

        TextField {
           id: txtFederationAccountPassword
            placeholderText: qsTr("Password")
            horizontalAlignment: TextInput.AlignHCenter
            echoMode: TextInput.Password
        }

        CheckBox {
            id: enable_sync
            text: qsTr("Enable sync")
            checked: false
        }

        Button {
            id: buttonCheckSettings
            Layout.alignment: Qt.AlignHCenter

            text: qsTr("Test Connection")
            flat: false
            onClicked: {
                network_settings.test_connection(txtFederationProtocol.text,
                                                 txtFederationServer.text,
                                                 txtFederationPort.text,
                                                 txtFederationAccount.text,
                                                 txtFederationAccountPassword.text
                                                 );
            }

        }


        Button {
            id: buttonSetSettings
            Layout.alignment: Qt.AlignHCenter
            text: qsTr("Done")
            flat: false
            onClicked: {
                network_settings.getvals(txtFederationServer.text,
                    txtFederationAccount.text, txtFederationAccountPassword.text,
                    enable_sync);
            }

        }
    }

}
