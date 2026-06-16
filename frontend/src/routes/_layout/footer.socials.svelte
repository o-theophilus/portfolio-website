<script>
	import { Button } from '$lib/button';

	let platforms = [
		{ name: 'whatsapp', href: 'https://wa.me/2348067397793/?text=Hello%20Theophilus' },
		{ name: 'twitter', href: 'https://twitter.com/o__theophilus' },
		{ name: 'github', href: 'https://github.com/o-theophilus' },
		// { name: "discord", href: 'https://discord.com/users/theophilus#6682' },
		{ name: 'facebook', href: 'https://m.facebook.com/o.theophilus' },
		// { name: "instagram", href: 'https://www.instagram.com/o_theophilus_/' },
		{ name: 'linkedin', href: 'https://www.linkedin.com/in/o-theophilus/' }
	];
</script>

<div class="line">
	{#each platforms as { name, href }}
		<Button icon={name} {href} target="_blank" --button-width="36px" --button-height="36px"
		></Button>
	{/each}
</div>

<style>
	.line {
		justify-content: center;
		gap: 2px;
	}
	@media screen and (min-width: 600px) {
		.line {
			justify-content: unset;
		}
	}
</style>
