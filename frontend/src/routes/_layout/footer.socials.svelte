<script>
	import { Icon } from '$lib/macro';
	import { Button } from '$lib/button';

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
		<Button {icon} {href} target="_blank" --button-width="36px" --button-height="36px"></Button>
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
