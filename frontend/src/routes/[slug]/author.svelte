<script>
	let author = {
		name: 'Theophilus Ogbolu'
	};

	let saturation = Math.floor(Math.random() * (360 + 1));
</script>

<section>
	<strong> Author </strong>
	<class class="block">
		<div
			class="img"
			class:light={saturation > 29 && saturation < 189}
			style:--saturation={saturation}
		>
			{author.name[0]}
		</div>
		<div class="name">{author.name}</div>
	</class>
</section>

<style>
	section {
		display: flex;
		flex-direction: column;
		gap: var(--sp2);
	}
	strong {
		color: var(--ac1);
	}
	.block {
		display: flex;
		gap: var(--sp2);
		align-items: center;
	}

	.img {
		--size: 40px;

		background-color: hsl(var(--saturation), 100%, 50%);
		border-radius: 50%;
		flex-shrink: 0;

		width: var(--size);
		height: var(--size);

		display: flex;
		align-items: center;
		justify-content: center;

		text-transform: capitalize;
		font-size: larger;
		font-weight: bold;

		color: var(--ac5_);
	}
	.light {
		color: var(--ac1_);
	}
</style>
