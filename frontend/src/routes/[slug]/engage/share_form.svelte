<script>
	import { page } from '$app/state';
	import { module, app } from '$lib/store.svelte.js';

	import { Button } from '$lib/button';
	import { Icon } from '$lib/macro';
	import { Form } from '$lib/layout';

	let title = `Check Out: ${module.value.title}`;

	let platforms = [
		{
			name: 'facebook',
			href: `https://www.facebook.com/sharer.php?u=${page.url.href}`
		},
		{
			name: 'twitter',
			href: `http://twitter.com/share?text=${title}&url=${page.url.href}&hashtags=portfolio,website`
		},
		{
			name: 'whatsapp',
			href: `whatsapp://send?text=${title}%20${page.url.href}`
		},
		{
			name: 'telegram',
			href: `https://telegram.me/share/url?url=${page.url.href}&text=${title}`
		}
	];

	const click = (on) => {
		fetch(`${import.meta.env.VITE_BACKEND}/log`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			},
			body: JSON.stringify({
				action: 'shared',
				entity_type: 'post',
				entity_key: module.post.key,
				misc: { on }
			})
		});
	};
</script>

<Form title="Share">
	<div class="line">
		{#each platforms as x}
			<Button
				target="_blank"
				title={x.name}
				onclick={() => {
					click(x.name);
				}}
				href={x.href}
			>
				<Icon icon={x.name} />
			</Button>
		{/each}
	</div>
</Form>
