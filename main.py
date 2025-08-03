import tkinter as tk
from tkinter import messagebox, scrolledtext
import threading
import asyncio
import discord
from discord.ext import commands
import logging

logging.basicConfig(level=logging.INFO)

# --- Bot Discord avec commandes principales ---
class DiscordBot(commands.Bot):
    def __init__(self, command_prefix, intents, log_func):
        super().__init__(command_prefix=command_prefix, intents=intents)
        self.log = log_func
        self.add_commands()

    def add_commands(self):
        @self.command()
        async def ping(ctx):
            await ctx.send("Pong!")
            self.log(f"[+] Commande ping utilisée par {ctx.author}")

        @self.command()
        async def crchannels(ctx):
            await ctx.send("Combien de salons voulez-vous créer ? (ex: 3)")

            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel

            try:
                msg_num = await self.wait_for('message', timeout=30.0, check=check)
                num_channels = int(msg_num.content)
                await ctx.send("Type de salon ? (text/voice)")
                msg_type = await self.wait_for('message', timeout=30.0, check=check)
                channel_type = msg_type.content.lower()
                await ctx.send("Nom des salons ?")
                msg_name = await self.wait_for('message', timeout=30.0, check=check)
                channel_name = msg_name.content

                created = []
                for _ in range(num_channels):
                    if channel_type == "text":
                        c = await ctx.guild.create_text_channel(channel_name)
                    elif channel_type == "voice":
                        c = await ctx.guild.create_voice_channel(channel_name)
                    else:
                        await ctx.send("Type de salon invalide, annulation.")
                        return
                    created.append(c)
                await ctx.send(f"{num_channels} salons '{channel_name}' de type {channel_type} créés.")
                self.log(f"[+] {num_channels} salons '{channel_name}' créés par {ctx.author}")
            except asyncio.TimeoutError:
                await ctx.send("Temps écoulé, commande annulée.")
                self.log("[!] crchannels annulé (timeout)")

        @self.command()
        async def spamchannels(ctx):
            await ctx.send("Combien de messages par salon ?")

            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel

            try:
                msg_num = await self.wait_for('message', timeout=30.0, check=check)
                num_messages = int(msg_num.content)
                await ctx.send("Contenu du message à spammer ?")
                msg_content = await self.wait_for('message', timeout=30.0, check=check)
                message_content = msg_content.content

                for channel in ctx.guild.text_channels:
                    for _ in range(num_messages):
                        try:
                            await channel.send(message_content)
                        except discord.Forbidden:
                            self.log(f"[-] Pas la permission d'envoyer dans {channel.name}")
                        except Exception as e:
                            self.log(f"[-] Erreur en envoyant dans {channel.name}: {e}")
                await ctx.send("Spam terminé.")
                self.log(f"[+] Spam dans tous les salons par {ctx.author}")
            except asyncio.TimeoutError:
                await ctx.send("Temps écoulé, commande annulée.")
                self.log("[!] spamchannels annulé (timeout)")

        @self.command()
        async def banall(ctx):
            no_ban_kick = []  # Ajouter ici les IDs à ne pas bannir si besoin
            members = [m for m in ctx.guild.members if not m.bot and m.id not in no_ban_kick]
            await ctx.send(f"Bannissement de {len(members)} membres...")

            for member in members:
                try:
                    await member.ban(reason="Banni par bot")
                except discord.Forbidden:
                    self.log(f"[-] Pas la permission de bannir {member}")
                except Exception as e:
                    self.log(f"[-] Erreur bannissement {member}: {e}")

            await ctx.send("Bannissement terminé.")
            self.log(f"[+] banall utilisé par {ctx.author}")

        @self.command()
        async def kickall(ctx):
            no_kick = []  # Ajouter ici les IDs à ne pas kicker si besoin
            members = [m for m in ctx.guild.members if not m.bot and m.id not in no_kick]
            await ctx.send(f"Expulsion de {len(members)} membres...")

            for member in members:
                try:
                    await member.kick(reason="Kické par bot")
                except discord.Forbidden:
                    self.log(f"[-] Pas la permission d'expulser {member}")
                except Exception as e:
                    self.log(f"[-] Erreur expulsion {member}: {e}")

            await ctx.send("Expulsion terminée.")
            self.log(f"[+] kickall utilisé par {ctx.author}")

        @self.command()
        async def dmmembers(ctx):
            await ctx.send("Message à envoyer à tous les membres ?")

            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel

            try:
                msg_content = await self.wait_for('message', timeout=60.0, check=check)
                message = msg_content.content

                members = [m for m in ctx.guild.members if not m.bot]
                count = 0
                for member in members:
                    try:
                        await member.send(message)
                        count += 1
                    except Exception:
                        pass
                await ctx.send(f"Message envoyé à {count} membres.")
                self.log(f"[+] dmmembers utilisé par {ctx.author}, message envoyé à {count} membres")
            except asyncio.TimeoutError:
                await ctx.send("Temps écoulé, commande annulée.")
                self.log("[!] dmmembers annulé (timeout)")

        @self.command()
        async def createroles(ctx):
            await ctx.send("Combien de rôles créer ?")

            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel

            try:
                msg_num = await self.wait_for('message', timeout=30.0, check=check)
                num_roles = int(msg_num.content)
                await ctx.send("Nom des rôles ?")
                msg_name = await self.wait_for('message', timeout=30.0, check=check)
                role_name = msg_name.content

                for _ in range(num_roles):
                    try:
                        await ctx.guild.create_role(name=role_name)
                    except Exception as e:
                        self.log(f"[-] Erreur création rôle: {e}")
                await ctx.send(f"{num_roles} rôles '{role_name}' créés.")
                self.log(f"[+] createroles utilisé par {ctx.author}")
            except asyncio.TimeoutError:
                await ctx.send("Temps écoulé, commande annulée.")
                self.log("[!] createroles annulé (timeout)")

        @self.command()
        async def servname(ctx):
            await ctx.send("Nouveau nom du serveur ?")

            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel

            try:
                msg_name = await self.wait_for('message', timeout=30.0, check=check)
                new_name = msg_name.content
                await ctx.guild.edit(name=new_name)
                await ctx.send(f"Nom du serveur changé en '{new_name}'.")
                self.log(f"[+] servname utilisé par {ctx.author}")
            except asyncio.TimeoutError:
                await ctx.send("Temps écoulé, commande annulée.")
                self.log("[!] servname annulé (timeout)")

        @self.command()
        async def webhookspam(ctx):
            await ctx.send("URL du webhook ?")

            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel

            try:
                msg_url = await self.wait_for('message', timeout=30.0, check=check)
                webhook_url = msg_url.content
                await ctx.send("Message à spammer ?")
                msg_content = await self.wait_for('message', timeout=30.0, check=check)
                message_content = msg_content.content

                webhook = discord.Webhook.from_url(webhook_url, adapter=discord.RequestsWebhookAdapter())
                for _ in range(5):  # spam 5 fois
                    webhook.send(message_content)
                await ctx.send("Spam webhook terminé.")
                self.log(f"[+] webhookspam utilisé par {ctx.author}")
            except Exception as e:
                await ctx.send(f"Erreur : {e}")
                self.log(f"[-] webhookspam erreur : {e}")

        @self.command()
        async def dlchannels(ctx):
            channels = ctx.guild.channels
            count = 0
            for channel in channels:
                try:
                    await channel.delete()
                    count +=1
                except Exception:
                    pass
            await ctx.send(f"{count} salons supprimés.")
            self.log(f"[+] dlchannels utilisé par {ctx.author}")

# --- Interface Tkinter ---
class BotGUI:
    def __init__(self, root):
        self.root = root
        root.title("Lanceur Bot Discord")
        root.geometry("600x450")

        self.token_label = tk.Label(root, text="Entrez le token du bot Discord :")
        self.token_label.pack(pady=5)

        self.token_entry = tk.Entry(root, width=70, show="*")
        self.token_entry.pack(pady=5)

        self.start_button = tk.Button(root, text="Lancer le bot", command=self.start_bot)
        self.start_button.pack(pady=10)

        self.log_text = scrolledtext.ScrolledText(root, height=20, state='disabled')
        self.log_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.bot_thread = None

    def log(self, message):
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')

    def start_bot(self):
        token = self.token_entry.get().strip()
        if not token:
            messagebox.showerror("Erreur", "Le token ne peut pas être vide.")
            return
        self.start_button.config(state='disabled')
        self.log("[*] Lancement du bot...")

        # Démarrer le bot dans un thread à part
        self.bot_thread = threading.Thread(target=self.run_bot, args=(token,), daemon=True)
        self.bot_thread.start()

    def run_bot(self, token):
        # Création explicite d'une boucle asyncio dans ce thread
        asyncio.set_event_loop(asyncio.new_event_loop())

        intents = discord.Intents.all()
        intents.members = True  # Nécessaire pour kick/ban, etc.

        bot = DiscordBot(command_prefix="+", intents=intents, log_func=self.log)

        try:
            bot.run(token)
        except discord.errors.LoginFailure:
            self.log("[!] Token invalide ou erreur de connexion.")
            self.enable_button()
        except Exception as e:
            self.log(f"[!] Erreur inattendue : {e}")
            self.enable_button()

    def enable_button(self):
        self.root.after(0, lambda: self.start_button.config(state='normal'))

# --- Lancement interface ---
if __name__ == "__main__":
    root = tk.Tk()
    app = BotGUI(root)
    root.mainloop()
