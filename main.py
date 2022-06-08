import tkinter
from tkinter import ttk
import tkinter.filedialog
import gmlParser
import plotly.graph_objects as go
import numpy as np

bigFontName = ("Arial bold", 19)
fontName = ("Arial", 13)

# program class
class program(tkinter.Tk):
    def __init__(self, *args, **kwargs):
        tkinter.Tk.__init__(self, *args, **kwargs)
        thisContainer = tkinter.Frame(self)
        thisContainer.pack(side="top", fill="both", expand=True)
        thisContainer.grid_rowconfigure(0, minsize=300, weight=1)
        thisContainer.grid_columnconfigure(0, minsize=300, weight=1)
        self.allFrames = self.initialization({}, thisContainer)
        self.frames(Menu)

    # method for initialization
    def initialization(self, frames, thisContainer):
        f = Menu(thisContainer, self)
        frames[Menu] = f
        f.grid(row=0, column=0, sticky='nsew')
        return frames

    # for frames
    def frames(self, j):
        frame = self.allFrames[j]
        frame.tkraise()


# Menu page
class Menu(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)
        controller.geometry("250x300")
        label = tkinter.Label(self, text="IndoorGML Viewer", font=bigFontName)
        label.grid(row=0, padx=10, pady=20)
        entryPath = tkinter.StringVar()
        entry = tkinter.Entry(self, textvariable=entryPath, font=fontName)
        entryPath.set("")
        entry.grid()
        b1 = tkinter.Button(self, text='Select IndoorGML file', font=fontName, relief='raised',
                            command=lambda entryPath=entryPath: self.path(entryPath, '.gml'))
        b1.grid(padx=20, pady=20)
        entryPathSIMOGenData = tkinter.StringVar()
        entry2 = ttk.Entry(self, textvariable=entryPathSIMOGenData, font=fontName)
        entryPathSIMOGenData.set("")
        entry2.grid()

        bStart = tkinter.Button(self, text="Start", font=fontName, bg='blue', fg='white',
                                command=lambda self=self, controller=controller, entryPath=entryPath : self.visualize(controller, entryPath,))
        bStart.grid(padx=30, pady=30)

    # returns the path of file
    def path(self, entryPath, inputType):
        f = tkinter.filedialog.askopenfilename(
            parent=self, initialdir='C:',
            title='Choose file',
            filetypes=[(inputType + ' files', inputType)]
        )
        entryPath.set(str(f))

    # close function
    def closeFunction(self, controller):
        controller.frames(Menu)

    # for visualization IndoorGML data
    def visualize(self, controller, pathGML):
        gmlFloors = gmlParser.myGML_3D(pathGML.get())
        x = []
        y = []
        z = []

        for myobject in gmlParser.GMLOBJ_3D_Objects:
            for i in (range(len(myobject.allPos) - 2)):
                temp = np.float64(myobject.allPos[i][0])
                temp2 = np.float64(myobject.allPos[i][1])
                temp3 = np.float64(myobject.allPos[i][2])
                tempX = np.float64(myobject.allPos[i + 1][0])
                temp2Y = np.float64(myobject.allPos[i + 1][1])
                temp3Z = np.float64(myobject.allPos[i + 1][2])
                x.append(temp)
                x.append(tempX)
                x.append(None)
                y.append(temp2)
                y.append(temp2Y)
                y.append(None)
                z.append(temp3)
                z.append(temp3Z)
                z.append(None)

        x2 = []
        y2 = []
        z2 = []
        for myobject in gmlParser.gmlObjectsDoors_3D:
            for i in (range(len(myobject.allPos) - 1)):
                temp = np.float64(myobject.allPos[i][0])
                temp2 = np.float64(myobject.allPos[i][1])
                temp3 = np.float64(myobject.allPos[i][2])
                tempX = np.float64(myobject.allPos[i + 1][0])
                temp2Y = np.float64(myobject.allPos[i + 1][1])
                temp3Z = np.float64(myobject.allPos[i + 1][2])
                x2.append(temp)
                x2.append(tempX)
                x2.append(None)
                y2.append(temp2)
                y2.append(temp2Y)
                y2.append(None)
                z2.append(temp3)
                z2.append(temp3Z)
                z2.append(None)

        trace = None

        config = {
            'displayModeBar': True,
            'displaylogo': False,
            'modeBarButtonsToRemove': ['zoom2d', 'hoverCompareCartesian', 'hoverClosestCartesian', 'toggleSpikelines']
        }

        fig = go.Figure(data=[
                                 go.Scatter3d(
                                     x=x,
                                     y=y,
                                     z=z,
                                     mode='lines',
                                     surfacecolor='#0000FF',
                                     line=dict(
                                         width=4,
                                         color='#0000FF'
                                     )),
                                 go.Scatter3d(
                                     x=x2,
                                     y=y2,
                                     z=z2,
                                     mode='lines',
                                     line=dict(
                                         width=6,
                                         color='#FFFF00',  # set color to an array/list of desired values
                                     ))
                             ] * 2,
                        layout=go.Layout({"title": "IndoorGML Viewer",
                                          'uirevision': True,
                                          "showlegend": True},
                                         ),
                        )

        updatemenus = [dict(
            type="buttons",
            buttons=[
                dict(label="Play",
                     method="animate",
                     args=[None, {"frame": {"duration": 5, "redraw": True},
                                  "fromcurrent": True,
                                  "transition": {"duration": 0}}]),

                {
                    "args": [[None], {"frame": {"duration": 0, "redraw": False},
                                      "mode": "immediate",
                                      "transition": {"duration": 0}}],
                    "label": "Pause",
                    "method": "animate"
                }

            ])]

        fig.update_yaxes(
            scaleanchor="x",
            scaleratio=1)

        fig.update_layout({
            'plot_bgcolor': 'rgba(0, 0, 0, 0)',
            'paper_bgcolor': 'rgba(0, 0, 0, 0)'
        })

        fig['layout'].update(updatemenus=updatemenus)
        fig.update_layout(scene_aspectmode='data')

        config = {
            'displayModeBar': True,
            'editable': True,
            'showLink': False,
            'displaylogo': False,
        }

        fig.show(config=config)



# main function
def main():
    app = program()
    app.mainloop()


if __name__ == "__main__":
    main()
