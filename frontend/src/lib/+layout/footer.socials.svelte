<script>
	import { Icon } from '$lib/macro';
	import { BackButton } from '$lib/button';

	let platforms = [
		{ icon: 'whatsapp', href: 'https://wa.me/2348067397793/?text=Hello%20Theophilus' },
		{ icon: 'twitter', href: 'https://twitter.com/o__theophilus' },
		{ icon: 'github', href: 'https://github.com/o-theophilus' },
		// { icon: "discord", href: 'https://discord.com/users/theophilus#6682' },
		{ icon: 'facebook', href: 'https://m.facebook.com/o.theophilus' },
		// { icon: "instagram", href: 'https://www.instagram.com/o_theophilus_/' },
		{ icon: 'linkedin', href: 'https://www.linkedin.com/in/o-theophilus/' }
	];
</script>

<div class="line">
	{#each platforms as { icon, href }}
		<a {href} target="_blank" rel="noopener noreferrer">
			<Icon {icon} size="20" />
		</a>
	{/each}
</div>

<style>
	.line {
		justify-content: center;
		gap: 4px;
	}
	@media screen and (min-width: 600px) {
		.line {
			justify-content: unset;
		}
	}

	a {
		--size: 32px;
		display: flex;
		justify-content: center;
		align-items: center;

		width: var(--size);
		height: var(--size);
		border-radius: 50%;

		background-color: transparent;
		fill: var(--ft2);

		transition:
			background-color var(--trans),
			fill var(--trans);
	}

	a:hover {
		background-color: var(--cl1);
		fill: white;
	}
</style>
