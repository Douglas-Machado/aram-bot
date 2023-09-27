import discord


class PaginationView(discord.ui.View):
    current_page: int = 1
    separator: int = 5

    async def send(self, ctx):
        self.message = await ctx.send(view=self)
        await self.update_message(self.data[: self.separator])

    def format_data(self, data):
        fields = [{"name": key} for key in data[0].keys()]
        for title in fields:
            title["value"] = ""
            title["inline"] = True
        count = 3
        for d in data:
            fields.insert(count, {"name": "", "value": d.get("name"), "inline": True})
            fields.insert(
                count + 1, {"name": "", "value": d.get("winrate"), "inline": True}
            )
            fields.insert(
                count + 2, {"name": "", "value": d.get("matches"), "inline": True}
            )
            count += 4
        return fields

    def create_embed(self, data):
        embed = discord.Embed()
        titles = self.format_data(data)
        embed_dict = {
            "title": f"best {len(self.data)} champions of patch 13.18",
            "description": f"page {self.current_page} of {int(len(self.data) / self.separator)}",
            "color": 0xFEE75C,
            "author": {
                "name": "ARAMID",
                "icon_url": "https://github.com/Douglas-Machado.png",
            },
            "fields": titles,
        }

        return embed.from_dict(embed_dict)

    async def update_message(self, data):
        self.update_buttons()
        await self.message.edit(embed=self.create_embed(data), view=self)

    def update_buttons(self):
        if self.current_page == 1:
            self.prev_button.disabled = True
            self.first_page_button.disabled = True
            self.first_page_button.style = discord.ButtonStyle.gray
            self.prev_button.style = discord.ButtonStyle.gray
        else:
            self.prev_button.disabled = False
            self.first_page_button.disabled = False
            self.first_page_button.style = discord.ButtonStyle.green
            self.prev_button.style = discord.ButtonStyle.primary

        if self.current_page == int(len(self.data) / self.separator):
            self.next_button.disabled = True
            self.last_page_button.disabled = True
            self.last_page_button.style = discord.ButtonStyle.gray
            self.next_button.style = discord.ButtonStyle.gray
        else:
            self.next_button.disabled = False
            self.last_page_button.disabled = False
            self.last_page_button.style = discord.ButtonStyle.green
            self.next_button.style = discord.ButtonStyle.primary

    @discord.ui.button(emoji="⏪", style=discord.ButtonStyle.primary)
    async def first_page_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.defer()
        self.current_page = 1
        until_item = self.current_page * self.separator
        from_item = until_item - self.separator
        self.data[from_item:until_item]
        await self.update_message(self.data[from_item:until_item])

    @discord.ui.button(emoji="◀️", style=discord.ButtonStyle.primary)
    async def prev_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.defer()
        self.current_page -= 1
        until_item = self.current_page * self.separator
        from_item = until_item - self.separator
        self.data[from_item:until_item]
        await self.update_message(self.data[from_item:until_item])

    @discord.ui.button(emoji="▶️", style=discord.ButtonStyle.primary)
    async def next_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.defer()
        self.current_page += 1
        until_item = self.current_page * self.separator
        from_item = until_item - self.separator
        await self.update_message(self.data[from_item:until_item])

    @discord.ui.button(emoji="⏩", style=discord.ButtonStyle.primary)
    async def last_page_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.defer()
        self.current_page = int(len(self.data) / self.separator)
        until_item = self.current_page * self.separator
        from_item = until_item - self.separator
        await self.update_message(self.data[from_item:until_item])
