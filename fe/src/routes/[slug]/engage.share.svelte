<script>
	import { page } from '$app/stores';
	import { module } from '$lib/store_old.js';
	import { token } from '$lib/cookie.js';

	import Button from '$lib/button_old/button.svelte';
	import Icon from '$lib/icon.svelte';

	let text = `Check Out: ${$module.post.title}`;

	let platforms = [
		{
			name: 'facebook',
			href: `https://www.facebook.com/sharer.php?u=${$page.url.href}`
		},
		{
			name: 'twitter',
			href: `http://twitter.com/share?text=${text}&url=${$page.url.href}&hashtags=portfolio,website`
		},
		{
			name: 'whatsapp',
			href: `whatsapp://send?text=${text}%20${$page.url.href}`
		},
		{
			name: 'telegram',
			href: `https://telegram.me/share/url?url=${$page.url.href}&text=${text}`
		}
	];

	const click = (on) => {
		fetch(`${import.meta.env.VITE_BACKEND}/log`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({
				action: 'shared',
				entity_type: 'post',
				entity_key: $module.post.key,
				misc: { on }
			})
		});
	};
</script>

<section class="content">
	<strong class="ititle"> Share </strong>
	<div class="line">
		{#each platforms as x}
			<Button
				target="_blank"
				title={x.name}
				on:click={() => {
					click(x.name);
				}}
				href={x.href}
			>
				<Icon icon={x.name} size="1.4" />
			</Button>
		{/each}
	</div>
</section>

<style>
	.content {
		display: flex;
		flex-direction: column;
		gap: var(--sp2);

		padding: var(--sp3);
	}

	.line {
		display: flex;
		gap: var(--sp1);
	}
</style>
