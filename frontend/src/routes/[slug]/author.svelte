<script>
	let author = {
		name: 'Theophilus Ogbolu'
	};

	let hue = Math.floor(Math.random() * (360 + 1));
</script>

<section>
	<div class="title">Author</div>
	<class class="block">
		<div class="img" class:light={hue > 29 && hue < 189} style:--hue={hue}>
			{author.name[0]}
		</div>
		{author.name}
	</class>
</section>

<style>
	section {
		display: flex;
		flex-direction: column;
		gap: var(--sp2);
	}

	.title {
		font-weight: 800;
		color: var(--ac1);
	}
	.block {
		display: flex;
		gap: var(--sp2);
		align-items: center;
	}

	.img {
		--size: 40px;

		display: flex;
		align-items: center;
		justify-content: center;
		flex-shrink: 0;

		width: var(--size);
		height: var(--size);
		border-radius: 50%;

		background-color: hsl(var(--hue), 100%, 50%);
		text-transform: capitalize;
		font-size: larger;
		font-weight: bold;

		color: var(--ac8_);
	}
	.light {
		color: var(--ac1_);
	}
</style>
