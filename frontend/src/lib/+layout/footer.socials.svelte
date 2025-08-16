<script>
	import { Icon } from '$lib/macro';
</script>

<div class="line">
	<a href="https://wa.me/2348067397793/?text=Hello%20Theophilus">
		<Icon icon="whatsapp" />
	</a>
	<a href="https://twitter.com/o__theophilus" target="_blank" rel="noopener noreferrer">
		<Icon icon="twitter" />
	</a>
	<a href="https://github.com/o-theophilus" target="_blank" rel="noopener noreferrer">
		<Icon icon="github" />
	</a>
	<!-- <a href="https://discord.com/users/theophilus#6682" target="_blank" rel="noopener noreferrer">
		<Icon icon="discord" />
	</a> -->
	<a href="https://m.facebook.com/o.theophilus" target="_blank" rel="noopener noreferrer">
		<Icon icon="facebook" />
	</a>
	<!-- <a href="https://www.instagram.com/o_theophilus_/" target="_blank" rel="noopener noreferrer">
		<Icon icon="instagram" />
	</a> -->
	<a href="https://www.linkedin.com/in/o-theophilus/" target="_blank" rel="noopener noreferrer">
		<Icon icon="linkedin" />
	</a>
</div>

<style>
	.line {
		justify-content: center;
		gap: var(--sp2);

		max-width: var(--mobileWidth);
	}
	@media screen and (min-width: 600px) {
		.line {
			justify-content: unset;
		}
	}

	a {
		--size: 20px;
		display: flex;
		justify-content: center;
		align-items: center;

		width: var(--size);
		height: var(--size);

		border-radius: 50%;

		color: var(--ft2);

		transition: color var(--trans);
	}

	a:hover {
		color: var(--cl1);
	}
</style>
