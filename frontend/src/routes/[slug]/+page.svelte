<script>
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { module, portal, user } from '$lib/store.js';

	import Content from '$lib/content.svelte';
	import Marked from '$lib/marked.svelte';
	import Meta from '$lib/meta.svelte';
	import Button from '$lib/button/button.svelte';
	import BRound from '$lib/button/round.svelte';
	import Tags from './tags.svelte';
	import Toggle from '$lib/toggle.svelte';
	import Icon from '$lib/icon.svelte';
	import Log from '$lib/log.svelte';

	import Title from './_title.svelte';
	import Description from './_description.svelte';
	import Edit_Tags from './_tags.svelte';
	import Edit_Content from './_content.svelte';
	import Edit_Date from './_date.svelte';
	import Edit_Status from './_status.svelte';
	import Manage_Photo from './_photo.svelte';
	import Manage_Video from './_video.svelte';

	import Share from './_share.svelte';
	import Rating from './_rating.svelte';

	import Comment from './comment/index.svelte';
	import Highlight from './highlight.svelte';
	import Author from './author.svelte';

	export let data;
	let { post } = data;
	let { ratings } = data;
	let o_rating = 0;
	let my_rating = 0;
	let content = '';
	let tags = [];
	let photo_count = 1;
	let video_count = 0;

	const calc_rating = () => {
		o_rating = 0;
		for (const i in ratings) {
			o_rating += ratings[i].rating;
			if (ratings[i].user_key == $user.key) {
				my_rating = ratings[i].rating;
			}
		}
	};
	calc_rating();

	$: if ($portal) {
		if ($portal.for == 'post') {
			post = $portal.data;
		} else if ($portal.for == 'rating') {
			ratings = $portal.data;
			calc_rating();
		}

		if (['post', 'rating'].includes($portal.for)) {
			$portal = {};
		}
	}

	$: if (post.content) {
		content = post.content;
		photo_count = 1;
		let exist = content.search(/{#photo}/) >= 0;
		while (exist) {
			let i = `![${post.title}](${post.photos[photo_count]})`;
			content = content.replace(/{#photo}/, i);
			exist = content.search(/{#photo}/) >= 0;
			photo_count = photo_count + 1;
		}

		video_count = 0;
		exist = content.search(/{#video}/) >= 0;
		while (exist) {
			let i = `<iframe
					width="100%"
					height="500px"
					frameborder="0"
					src="https://www.youtube.com/embed/${post.videos[video_count]}">
				</iframe>
				`;
			content = content.replace(/{#video}/, i);
			exist = content.search(/{#video}/) >= 0;
			video_count = video_count + 1;
		}
	}

	let edit_mode = false;

	let is_admin = $user.permissions.some((x) =>
		[
			'post:edit_photos',
			'post:edit_videos',
			'post:edit_title',
			'post:edit_date',
			'post:edit_description',
			'post:edit_content',
			'post:edit_tags',
			'post:edit_status'
		].includes(x)
	);

	onMount(() => {
		if ($page.url.searchParams.has('edit') && is_admin) {
			$page.url.searchParams.delete('edit');
			edit_mode = true;

			window.history.replaceState(history.state, '', $page.url.href);
		}
	});
</script>

<Log action={'viewed'} entity_key={post.key} entity_type={'post'} />
<Meta title={post.title} description={post.description} image={post.photos[0]} />

<Content>
	{#if is_admin}
		<div class="toggle">
			<Toggle
				state_1="off"
				state_2="edit"
				active={edit_mode}
				on:click={() => {
					edit_mode = !edit_mode;
				}}
			/>
		</div>
	{/if}
	<div class="img">
		<img src={post.photos[0] || ''} alt={post.title} onerror="this.src='/site/no_photo.png'" />
		<div class="line">
			{#if $user.permissions.includes('post:edit_photos') && edit_mode}
				<BRound
					icon="photo"
					on:click={() => {
						$module = {
							module: Manage_Photo,
							post,
							photo_count
						};
					}}
				/>
			{/if}

			{#if video_count > 0 && $user.permissions.includes('post:edit_videos') && edit_mode}
				<BRound
					icon="movie"
					on:click={() => {
						$module = {
							module: Manage_Video,
							post,
							video_count
						};
					}}
				/>
			{/if}
		</div>
	</div>

	<div class="ititle">
		{#if $user.permissions.includes('post:edit_title') && edit_mode}
			<BRound
				icon="edit"
				on:click={() => {
					$module = {
						module: Title,
						post
					};
				}}
			/>
		{/if}
		<strong>
			{post.title}
		</strong>
	</div>

	{#if $user.permissions.includes('post:edit_date') && edit_mode}
		<hr />
		<BRound
			icon="edit"
			on:click={() => {
				$module = {
					module: Edit_Date,
					post
				};
			}}
		/>
	{/if}
	<span class="date">{post.date}</span>

	{#if $user.permissions.includes('post:edit_description') && edit_mode}
		<hr />
		<BRound
			icon="edit"
			icon_size={15}
			on:click={() => {
				$module = {
					module: Description,
					post
				};
			}}
		/>
		<div class="margin">
			{#if post.description}
				{post.description}
			{:else}
				No description
			{/if}
		</div>
	{/if}

	{#if $user.permissions.includes('post:edit_content') && edit_mode}
		<hr />
		<BRound
			icon="edit"
			icon_size={15}
			on:click={() => {
				$module = {
					module: Edit_Content,
					post
				};
			}}
		/>
	{/if}
	{#if post.content}
		<Marked md={content} />
		<br />
	{:else if edit_mode}
		<div class="margin">No content</div>
	{/if}

	<div class="line">
		<Button
			size="small"
			on:click={() => {
				$module = {
					module: Share,
					post
				};
			}}
		>
			<Icon icon="share" />
			Share
		</Button>

		{#if $user.login}
			<Button
				size="small"
				on:click={() => {
					$module = {
						module: Rating,
						post_key: post.key,
						ratings
					};
				}}
			>
				<Icon icon="hotel_class" />
				Rate: {my_rating} | Overall Rating: {o_rating}
			</Button>
		{/if}
	</div>
	<hr />

	<Author {post} />

	{#if post.tags.length > 0 || ($user.permissions.includes('post:edit_tags') && edit_mode)}
		<hr />
	{/if}

	{#if $user.permissions.includes('post:edit_tags') && edit_mode}
		<BRound
			icon="edit"
			icon_size={15}
			on:click={() => {
				$module = {
					module: Edit_Tags,
					post,
					tags_in: tags
				};
			}}
		/>
	{/if}

	{#if post.tags.length > 0}
		<Tags tags={post.tags} />
	{:else if edit_mode}
		<div class="margin">No tag</div>
	{/if}

	{#if $user.permissions.includes('post:edit_status') && edit_mode}
		<hr />
		<div class="line">
			<Button
				size="small"
				on:click={() => {
					$module = {
						module: Edit_Status,
						post
					};
				}}
			>
				<Icon icon="edit" size="16" />
				|
				<span>
					Status: <strong>{post.status}</strong>
				</span>
			</Button>
			{#if post.status == 'publish'}
				<Highlight {post} />
			{/if}
		</div>
	{/if}

	<hr />

	<Comment {post} />
</Content>

<style>
	.img {
		position: relative;
	}

	img {
		display: block;

		width: 100%;
		margin: var(--sp2) 0;
		border-radius: var(--sp1);

		background-color: var(--bg2);
	}
	.img .line {
		position: absolute;
		bottom: var(--sp1);
		left: var(--sp1);
	}

	.ititle {
		margin-top: var(--sp3);
	}
	.date {
		font-size: small;
		margin-bottom: var(--sp3);
	}

	.margin {
		margin: var(--sp2) 0;
	}

	hr {
		margin: var(--sp2) 0;
	}

	.line {
		display: flex;
		gap: var(--sp1);
	}
</style>
