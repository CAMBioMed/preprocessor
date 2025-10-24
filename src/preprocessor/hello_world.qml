import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Window {
    width: 300
    height: 200
    visible: true
    title: "Hello World"

    readonly property list<string> texts: ["Hallo Welt", "Hei maailma",
                                           "Hola Mundo", "Привет мир"]

    function setText() {
        var i = Math.round(Math.random() * 3)
        text.text = texts[i]
    }

    ColumnLayout {
        anchors.fill:  parent

        Image {
            id: logo
            // Use an image provider (registered as "cvimg" in Python). The provider will supply the image under the id "current".
            source: "image://cvimg/currents"
            fillMode: Image.PreserveAspectFit
            Layout.alignment: Qt.AlignHCenter
            Layout.preferredHeight: 100
            // Make sure width follows the parent layout width
            // width: parent ? parent.width : 200
            Layout.maximumHeight: 200
            Layout.maximumWidth: 200
        }

        Text {
            id: text
            text: "Hello World"
            Layout.alignment: Qt.AlignHCenter
        }
        Button {
            text: "Click me"
            Layout.alignment: Qt.AlignHCenter
            onClicked:  setText()
        }
    }
}
