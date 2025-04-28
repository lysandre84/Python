#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=====================================================================================================================================================


 /$$   /$$             /$$                                       /$$               /$$$$$$                      /$$                                        
| $$$ | $$            | $$                                      | $$              /$$__  $$                    | $$                                        
| $$$$| $$  /$$$$$$  /$$$$$$   /$$  /$$  /$$  /$$$$$$   /$$$$$$ | $$   /$$       | $$  \ $$ /$$$$$$$   /$$$$$$ | $$ /$$   /$$ /$$$$$$$$  /$$$$$$   /$$$$$$ 
| $$ $$ $$ /$$__  $$|_  $$_/  | $$ | $$ | $$ /$$__  $$ /$$__  $$| $$  /$$//$$$$$$| $$$$$$$$| $$__  $$ |____  $$| $$| $$  | $$|____ /$$/ /$$__  $$ /$$__  $$
| $$  $$$$| $$$$$$$$  | $$    | $$ | $$ | $$| $$  \ $$| $$  \__/| $$$$$$/|______/| $$__  $$| $$  \ $$  /$$$$$$$| $$| $$  | $$   /$$$$/ | $$$$$$$$| $$  \__/
| $$\  $$$| $$_____/  | $$ /$$| $$ | $$ | $$| $$  | $$| $$      | $$_  $$        | $$  | $$| $$  | $$ /$$__  $$| $$| $$  | $$  /$$__/  | $$_____/| $$      
| $$ \  $$|  $$$$$$$  |  $$$$/|  $$$$$/$$$$/|  $$$$$$/| $$      | $$ \  $$       | $$  | $$| $$  | $$|  $$$$$$$| $$|  $$$$$$$ /$$$$$$$$|  $$$$$$$| $$      
|__/  \__/ \_______/   \___/   \_____/\___/  \______/ |__/      |__/  \__/       |__/  |__/|__/  |__/ \_______/|__/ \____  $$|________/ \_______/|__/      
                                                                                                                    /$$  | $$                              
                                                                                                                   |  $$$$$$/                              
                                                                                                                    \______/                                           
=====================================================================================================================================================
=====================================================================================================================================================
 Script     : Network_Analyzer.py
 Auteur     : Lysius
 Date       : XX/XX/XXXX
 Description: Analyzer (bêta) - Gestion du réseau 
=====================================================================================================================================================
"""
import ipaddress
import sys
import csv
import threading
import subprocess
import socket
import whois
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext, TclError
import math
import platform

# Packet sniffing pour la surveillance du trafic
try:
    from scapy.all import sniff, IP
    SCAPY = True
except ImportError:
    SCAPY = False

# En option : ttkbootstrap pour les thèmes modernes
try:
    import ttkbootstrap as tb
    ThemeRoot = tb.Window
    STYLE = True
except ImportError:
    ThemeRoot = tk.Tk
    STYLE = False

# --- Network utilities ---
def ipv4_class(net: ipaddress.IPv4Network) -> str:
    first = int(str(net.network_address).split('.')[0])
    if 1 <= first <= 126: return "A"
    if 128 <= first <= 191: return "B"
    if 192 <= first <= 223: return "C"
    if 224 <= first <= 239: return "D (multicast)"
    return "E (reserved)"

def wildcard_mask(net: ipaddress.IPv4Network) -> str:
    return '.'.join(str(255 - int(o)) for o in str(net.netmask).split('.'))

def best_prefix_for_subnets(net: ipaddress._BaseNetwork, wanted: int) -> int:
    bits = math.ceil(math.log2(wanted))
    return min(net.max_prefixlen, net.prefixlen + bits)

def best_prefix_for_hosts(net: ipaddress._BaseNetwork, wanted: int) -> int:
    for p in range(net.prefixlen, net.max_prefixlen + 1):
        cap = (2 ** (net.max_prefixlen - p)) - (2 if isinstance(net, ipaddress.IPv4Network) else 0)
        if cap >= wanted: return p
    raise ValueError("Too many hosts")

def best_prefix_for_supernets(net: ipaddress._BaseNetwork, wanted: int) -> int:
    bits = math.ceil(math.log2(wanted))
    return max(0, net.prefixlen - bits)

class NetworkAnalyzer(ThemeRoot):
    def __init__(self):
        super().__init__()
        self.title("Network Analyzer Pro – IPv4 & IPv6")
        self.geometry("1200x1000")
        self.minsize(1150, 950)
        self.monitoring = False
        self.traffic_counts = {}
        self.last_report = None
        self._init_style()
        self._build_ui()

    def _init_style(self):
        if STYLE:
            style = tb.Style("cosmo")
            self.available_themes = style.theme_names()
            self.current_theme = style.theme_use()
        else:
            self.available_themes = ["default", "clam"]
            self.current_theme = "default"
            self.configure(bg="#2b2b2b")

    def _build_ui(self):
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        tabs = [
            ("Analyse Réseau", self._build_analyze_tab),
            ("Outils Réseau",  self._build_tools_tab),
            ("Logs",           self._build_logs_tab),
            ("Traffic",        self._build_traffic_tab),
            ("Paramètres",     self._build_settings_tab),
        ]
        for title, builder in tabs:
            frame = ttk.Frame(notebook)
            notebook.add(frame, text=title)
            builder(frame)

        self.status = ttk.Label(self, text="Prêt", relief=tk.SUNKEN, anchor="w")
        self.status.pack(fill="x", side=tk.BOTTOM)

    # --- Analyse Réseau ---
    def _build_analyze_tab(self, parent):
        frm = ttk.LabelFrame(parent, text="Paramètres d'Analyse")
        frm.pack(fill="x", padx=10, pady=10)
        ttk.Label(frm, text="Réseau (ex : 192.168.1.0/24) :").grid(row=0, column=0, sticky="e")
        self.net_entry = ttk.Entry(frm, width=30)
        self.net_entry.grid(row=0, column=1, padx=5, pady=5)

        self.analyze_mode = tk.StringVar(value="prefix")
        opts = [("Préfixe","prefix"),("Sous-réseaux","subnets"),
                ("Hôtes","hosts"),("Supernet","supernet")]
        for i,(t,v) in enumerate(opts):
            ttk.Radiobutton(frm,text=t,variable=self.analyze_mode,value=v)\
                .grid(row=1+i//2,column=i%2,sticky="w",padx=5,pady=2)

        ttk.Label(frm, text="Valeur :").grid(row=3, column=0, sticky="e")
        self.value_entry = ttk.Entry(frm, width=10)
        self.value_entry.grid(row=3, column=1, sticky="w")

        self.list_hosts = tk.BooleanVar()
        ttk.Checkbutton(frm,text="Lister hôtes (IPv4)",variable=self.list_hosts)\
            .grid(row=4,column=0,columnspan=2,sticky="w",pady=5)

        bf = ttk.Frame(parent); bf.pack(fill="x", padx=10, pady=5)
        for t,cmd in [("Analyser",self.analyze_network),
                      ("Export TXT",self.export_txt),
                      ("Export CSV",self.export_csv),
                      ("Copier",self.copy_clipboard)]:
            ttk.Button(bf,text=t,command=cmd).pack(side="left",padx=5)

        self.report_box = scrolledtext.ScrolledText(parent,height=20)
        self.report_box.pack(fill="both",expand=True,padx=10,pady=5)

    def analyze_network(self):
        net_str = self.net_entry.get().strip()
        if not net_str:
            messagebox.showwarning("Entrée manquante","Veuillez saisir un réseau.")
            return
        try:
            net = ipaddress.ip_network(net_str, strict=False)
        except ValueError as e:
            messagebox.showerror("Erreur réseau",str(e)); return

        m,val = self.analyze_mode.get(), self.value_entry.get().strip()
        new_p = net.prefixlen
        try:
            if m=="prefix" and val:      new_p = int(val)
            elif m=="subnets":           new_p = best_prefix_for_subnets(net,int(val))
            elif m=="hosts":             new_p = best_prefix_for_hosts(net,int(val))
            elif m=="supernet":          new_p = best_prefix_for_supernets(net,int(val))
        except:
            messagebox.showerror("Erreur valeur","Valeur invalide."); return

        out=[f"Analyse de : {net}","-"*60,
             f"IP Version      : IPv{net.version}",
             f"Network Addr    : {net.network_address}",
             f"CIDR/Mask       : /{net.prefixlen}  ({net.netmask})"]
        if net.version==4:
            out+= [f"Wildcard Mask   : {wildcard_mask(net)}",
                   f"Class IPv4      : {ipv4_class(net)}"]
        out+= [f"Total Addrs     : {net.num_addresses}",
               f"Usable Hosts    : {net.num_addresses - (2 if net.version==4 else 0)}"]
        if net.version==4:
            hosts = list(net.hosts())
            out+= [f"Broadcast       : {net.broadcast_address}",
                   f"Host Range      : {hosts[0]} – {hosts[-1]}"]

        if new_p!=net.prefixlen:
            if new_p>net.prefixlen:
                subs=list(net.subnets(new_prefix=new_p))
                out.append(f"\nSubnetting /{new_p} → {len(subs)} subnets")
                for idx,s in enumerate(subs[:100]):
                    line=f"{idx+1:>3}: {s}"
                    if self.list_hosts.get() and s.num_addresses<=256:
                        line+="  →  "+", ".join(str(h) for h in s.hosts())
                    out.append(line)
                if len(subs)>100:
                    out.append(f"... {len(subs)-100} more")
            else:
                sup=net.supernet(new_prefix=new_p)
                out.append(f"\nSupernet /{new_p} : {sup}")

        self.last_report="\n".join(out)
        self.report_box.config(state="normal")
        self.report_box.delete("1.0",tk.END)
        self.report_box.insert(tk.END,self.last_report)
        self.report_box.config(state="disabled")

    def export_txt(self):
        if not self.last_report:
            messagebox.showinfo("Aucun résultat","Aucune analyse à exporter."); return
        p=filedialog.asksaveasfilename(defaultextension=".txt",filetypes=[("Text","*.txt")])
        if p:
            with open(p,"w",encoding="utf-8") as f: f.write(self.last_report)
            messagebox.showinfo("Export TXT",f"Saved to {p}")

    def export_csv(self):
        if not self.last_report:
            messagebox.showinfo("Aucun résultat","Aucune analyse à exporter."); return
        p=filedialog.asksaveasfilename(defaultextension=".csv",filetypes=[("CSV","*.csv")])
        if p:
            with open(p,"w",newline="",encoding="utf-8") as f:
                w=csv.writer(f)
                for l in self.last_report.splitlines(): w.writerow([l])
            messagebox.showinfo("Export CSV",f"Saved to {p}")

    def copy_clipboard(self):
        if not self.last_report:
            messagebox.showinfo("Aucun résultat","Aucune analyse à copier."); return
        self.clipboard_clear(); self.clipboard_append(self.last_report)
        messagebox.showinfo("Copié","Rapport copié.")

    # --- Outils Réseau & Infos IP ---
    def _build_tools_tab(self,parent):
        frm=ttk.LabelFrame(parent,text="Outils Réseau & Infos IP")
        frm.pack(fill="x",padx=10,pady=10)
        ttk.Label(frm,text="Host/IP :").grid(row=0,column=0,sticky="e")
        self.host_entry=ttk.Entry(frm,width=30); self.host_entry.grid(row=0,column=1,padx=5,pady=5)
        ttk.Label(frm,text="Scan ports (e.g. 22,80,1000-2000) :")\
            .grid(row=1,column=0,sticky="e")
        self.port_entry=ttk.Entry(frm,width=30); self.port_entry.grid(row=1,column=1,padx=5,pady=5)

        tools=[("Ping",self._threaded(self.ping)),
               ("Trace",self._threaded(self.traceroute)),
               ("DNS",self._threaded(self.dns_lookup)),
               ("WHOIS",self._threaded(self.whois_query)),
               ("Info IP",self._threaded(self.ip_info))]
        for i,(t,c) in enumerate(tools):
            ttk.Button(frm,text=t,command=c).grid(row=2,column=i,padx=5,pady=5)

        self.tools_box=scrolledtext.ScrolledText(parent,height=20)
        self.tools_box.pack(fill="both",expand=True,padx=10,pady=5)

    def ping(self):
        h=self.host_entry.get().strip(); 
        if not h: return
        param='-n' if platform.system().lower().startswith('win') else '-c'
        cmd=['ping',param,'1',h]
        self.status.config(text=f"Pinging {h}…")
        try: out=subprocess.check_output(cmd,universal_newlines=True)
        except Exception as e: out=str(e)
        self.tools_box.insert(tk.END,f"\n--- Ping {h} ---\n{out}\n")
        self.status.config(text="Prêt")

    def traceroute(self):
        h=self.host_entry.get().strip()
        if not h: return
        prog='tracert' if platform.system().lower().startswith('win') else 'traceroute'
        self.status.config(text=f"Tracing {h}…")
        try:
            p=subprocess.Popen([prog,h],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            out,_=p.communicate(); out=out.decode()
        except Exception as e: out=str(e)
        self.tools_box.insert(tk.END,f"\n--- Trace {h} ---\n{out}\n")
        self.status.config(text="Prêt")

    def dns_lookup(self):
        h=self.host_entry.get().strip(); 
        if not h: return
        self.status.config(text=f"Resolving DNS {h}…")
        try:
            res=socket.getaddrinfo(h,None)
            out="\n".join(r[4][0] for r in res)
        except Exception as e: out=str(e)
        self.tools_box.insert(tk.END,f"\n--- DNS {h} ---\n{out}\n")
        self.status.config(text="Prêt")

    def whois_query(self):
        h=self.host_entry.get().strip()
        if not h: return
        self.status.config(text=f"WHOIS {h}…")
        try: out=str(whois.whois(h))
        except Exception as e: out=str(e)
        self.tools_box.insert(tk.END,f"\n--- WHOIS {h} ---\n{out}\n")
        self.status.config(text="Prêt")

    def ip_info(self):
        h=self.host_entry.get().strip()
        if not h: return
        info=[f"=== Infos sur {h} ==="]
        try:
            cn,al,ips=socket.gethostbyname_ex(h)
            info.append(f"IP : {', '.join(ips)}")
            info.append(f"Nom canonique : {cn}")
        except Exception as e:
            info.append(f"DNS error: {e}")
        try:
            rd=socket.gethostbyaddr(h)[0]
            info.append(f"Reverse DNS : {rd}")
        except: pass
        info.append("Masque par défaut : /32")
        # TTL from ping
        try:
            param='-n' if platform.system().lower().startswith('win') else '-c'
            p=subprocess.Popen(['ping',param,'1',h],stdout=subprocess.PIPE)
            out,_=p.communicate()
            for l in out.decode().splitlines():
                if 'ttl=' in l.lower():
                    info.append(f"TTL info: {l.strip()}")
        except: pass
        # port scan
        ps=self.port_entry.get().strip()
        ports=[]
        if ps:
            for part in ps.split(','):
                if '-' in part:
                    a,b=map(int,part.split('-'))
                    ports.extend(range(a,b+1))
                else:
                    ports.append(int(part))
        else:
            ports=[21,22,23,25,53,80,110,139,143,443,445,3389]
        openp=[]
        for pnum in ports:
            s=socket.socket(); s.settimeout(0.5)
            if s.connect_ex((h,pnum))==0: openp.append(pnum)
            s.close()
        info.append(f"Ports ouverts: {openp if openp else 'aucun'}")

        self.tools_box.insert(tk.END,"\n".join(info)+"\n")

    # --- Logs ---
    def _build_logs_tab(self,parent):
        bf=ttk.Frame(parent); bf.pack(fill="x",padx=10,pady=5)
        ttk.Button(bf,text="Importer CSV",command=self.import_logs).pack(side="left",padx=5)
        ttk.Button(bf,text="Exporter CSV",command=self.export_logs).pack(side="left",padx=5)
        self.logs_box=scrolledtext.ScrolledText(parent,height=30)
        self.logs_box.pack(fill="both",expand=True,padx=10,pady=5)

    def import_logs(self):
        p=filedialog.askopenfilename(filetypes=[('CSV','*.csv')])
        if not p: return
        with open(p,newline='',encoding='utf-8') as f:
            for row in csv.reader(f):
                self.logs_box.insert(tk.END,', '.join(row)+"\n")

    def export_logs(self):
        p=filedialog.asksaveasfilename(defaultextension='.csv',
                                       filetypes=[('CSV','*.csv')])
        if not p: return
        with open(p,'w',newline='',encoding='utf-8') as f:
            w=csv.writer(f)
            for l in self.logs_box.get('1.0',tk.END).splitlines():
                w.writerow([l])
        messagebox.showinfo('Export Logs',f'Enregistré : {p}')

    # --- Traffic & Control ---
    def _build_traffic_tab(self,parent):
        frm=ttk.LabelFrame(parent,text="Traffic & Control")
        frm.pack(fill="both",expand=True,padx=10,pady=10)
        if not platform.system().lower().startswith('win'):
            hf=ttk.Frame(frm); hf.pack(fill="x",pady=5)
            ttk.Label(hf,text="Interface :").pack(side="left",padx=5)
            self.iface=ttk.Combobox(hf,values=self._list_ifaces(),state="readonly")
            self.iface.set(self.iface['values'][0] if self.iface['values'] else 'eth0')
            self.iface.pack(side="left",padx=5)
        cols=("IP","Bytes")
        self.tree=ttk.Treeview(frm,columns=cols,show="headings")
        for c in cols:
            self.tree.heading(c,text=c); self.tree.column(c,anchor="center")
        self.tree.pack(fill="both",expand=True,padx=5,pady=5)
        cf=ttk.Frame(frm); cf.pack(fill="x",pady=5)
        ttk.Label(cf,text="Limite (kbps) :").pack(side="left",padx=5)
        self.kbps=ttk.Entry(cf,width=10); self.kbps.pack(side="left",padx=5)
        for txt,cmd in [("Limiter IP",self.limit_ip),("Retirer limite",self.unlimit_ip),
                        ("Bloquer IP",self.block_ip),("Débloquer IP",self.unblock_ip)]:
            ttk.Button(cf,text=txt,command=cmd).pack(side="left",padx=5)
        sf=ttk.Frame(frm); sf.pack(pady=5)
        self.start_btn=ttk.Button(sf,text="Démarrer Monitor",command=self.start_monitor)
        self.start_btn.pack(side="left",padx=5)
        self.stop_btn =ttk.Button(sf,text="Arrêter Monitor",command=self.stop_monitor,state="disabled")
        self.stop_btn.pack(side="left",padx=5)

    def _list_ifaces(self):
        try:
            out=subprocess.check_output(["ls","/sys/class/net"],universal_newlines=True)
            return out.strip().split()
        except:
            return ['eth0']

    def start_monitor(self):
        if not SCAPY:
            messagebox.showerror("Erreur","scapy requis pour trafic."); return
        self.monitoring=True
        self.start_btn.config(state="disabled"); self.stop_btn.config(state="normal")
        self.traffic_counts.clear()
        threading.Thread(target=self._sniff_packets,daemon=True).start()
        self._update_tree()

    def stop_monitor(self):
        self.monitoring=False
        self.start_btn.config(state="normal"); self.stop_btn.config(state="disabled")

    def _sniff_packets(self):
        sniff(prn=self._packet_handler,store=False)

    def _packet_handler(self,pkt):
        if IP in pkt:
            s,p=pkt[IP].src,pkt[IP].dst
            size=len(pkt)
            for ip in (s,p):
                self.traffic_counts[ip]=self.traffic_counts.get(ip,0)+size

    def _update_tree(self):
        if not self.monitoring: return
        sel_ips={self.tree.item(i)['values'][0] for i in self.tree.selection()}
        for i in self.tree.get_children(): self.tree.delete(i)
        def keyf(item):
            ip,c=item; parts=tuple(int(x) for x in ip.split('.') if x.isdigit()); return (parts,-c)
        for ip,c in sorted(self.traffic_counts.items(),key=keyf):
            iid=self.tree.insert('','end',values=(ip,c))
            if ip in sel_ips: self.tree.selection_add(iid)
        self.after(1000,self._update_tree)

    def limit_ip(self):
        sel=self.tree.selection(); rate=self.kbps.get().strip()
        if not sel or not rate.isdigit(): messagebox.showwarning("Entrée","IP + limite req."); return
        ip=self.tree.item(sel[0])['values'][0]
        if platform.system().lower().startswith('win'):
            messagebox.showerror("Non supporté","Limitation Win non supportée."); return
        dev=self.iface.get()
        subprocess.call(["tc","qdisc","del","dev",dev,"root"],stderr=subprocess.DEVNULL)
        cmd=["tc","qdisc","add","dev",dev,"root","tbf","rate",f"{rate}kbit","burst","32kbit","latency","400ms"]
        try: subprocess.check_call(cmd); messagebox.showinfo("Limité",f"{ip} à {rate}kbps")
        except Exception as e: messagebox.showerror("Erreur",str(e))

    def unlimit_ip(self):
        if platform.system().lower().startswith('win'):
            messagebox.showerror("Non supporté","Unlimit Win non supporté."); return
        dev=self.iface.get()
        try: subprocess.check_call(["tc","qdisc","del","dev",dev,"root"]); messagebox.showinfo("Unlimit","Retiré")
        except Exception as e: messagebox.showerror("Erreur",str(e))

    def block_ip(self):
        sel=self.tree.selection()
        if not sel: messagebox.showwarning("Sélection","Aucun IP."); return
        ip=self.tree.item(sel[0])['values'][0]
        if platform.system().lower().startswith('win'):
            cmd=["netsh","advfirewall","firewall","add","rule",f"name=Block_{ip}","dir=in","action=block",f"remoteip={ip}"]
        else:
            cmd=["iptables","-A","INPUT","-s",ip,"-j","DROP"]
        try: subprocess.check_call(cmd); messagebox.showinfo("Bloqué",ip)
        except Exception as e: messagebox.showerror("Erreur",str(e))

    def unblock_ip(self):
        sel=self.tree.selection()
        if not sel: messagebox.showwarning("Sélection","Aucun IP."); return
        ip=self.tree.item(sel[0])['values'][0]
        if platform.system().lower().startswith('win'):
            cmd=["netsh","advfirewall","firewall","delete","rule",f"name=Block_{ip}"]
        else:
            cmd=["iptables","-D","INPUT","-s",ip,"-j","DROP"]
        try: subprocess.check_call(cmd); messagebox.showinfo("Débloqué",ip)
        except Exception as e: messagebox.showerror("Erreur",str(e))

    # --- Paramètres / Thèmes ---
    def _build_settings_tab(self,parent):
        frm=ttk.LabelFrame(parent,text="Thèmes"); frm.pack(fill="both",expand=True,padx=10,pady=10)
        ttk.Label(frm,text="Thème :").grid(row=0,column=0,sticky="w")
        self.theme_cb=ttk.Combobox(frm,values=self.available_themes,state="readonly")
        self.theme_cb.set(self.current_theme); self.theme_cb.grid(row=0,column=1,padx=5)
        ttk.Button(frm,text="Appliquer",command=self.apply_theme).grid(row=0,column=2,padx=5)

    def apply_theme(self):
        if STYLE:
            sel=self.theme_cb.get()
            try: tb.Style(sel); self.status.config(text=f"Thème : {sel}")
            except TclError: messagebox.showerror("Thème invalide",f"\"{sel}\"")
        else:
            messagebox.showinfo("Non supporté","ttkbootstrap non installé")

    def _threaded(self,fn): return lambda: threading.Thread(target=fn,daemon=True).start()

if __name__ == '__main__':
    try:
        app=NetworkAnalyzer()
        app.mainloop()
    except KeyboardInterrupt:
        sys.exit(0)
